#!/usr/bin/env python3
"""Build self-verifying C binding contracts against a clean mruby/c source copy."""

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "mruby-idiomatic/scripts"))
import probe_mrubyc as probe


def read_expected(path):
    expected = json.loads(path.read_text())
    if (not isinstance(expected, list) or not expected or
            any(not isinstance(line, str) or not line.startswith("PASS ") or
                line.strip() != line or line.splitlines() != [line] for line in expected)):
        raise ValueError("expected must be a nonempty list of PASS lines")
    if len(set(expected)) != len(expected) or "PASS ALL binding-contract" not in expected:
        raise ValueError("expected requires unique checks and the completion marker")
    return expected


def classify_run(run, expected):
    compilation = run["compile"]
    runtime = run.get("run")
    if compilation["timed_out"] or compilation["exit_code"] != 0:
        return probe.classify("binding-contract", compilation, runtime)
    if runtime is None:
        raise ValueError("runtime is required after successful compilation")
    if runtime["timed_out"] or runtime["exit_code"] != 0:
        return probe.classify("binding-contract", compilation, runtime)
    actual = Counter(runtime["stdout"].splitlines())
    wanted = Counter(expected)
    if runtime["stderr"] or actual != wanted:
        return "FAIL", 0, "check output mismatch; missing=" + repr(list((wanted - actual).elements())) + "; extra=" + repr(list((actual - wanted).elements())) + "; stderr=" + repr(runtime["stderr"])
    return "PASS", 0, "PASS binding-contract"


def evaluate(runs, expected):
    if not runs:
        raise ValueError("at least one execution is required")
    rows = [classify_run(run, expected) for run in runs]
    identical = all(row == rows[0] for row in rows)
    return rows, identical, identical and all(row[0] == "PASS" for row in rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mrubyc", required=True, type=Path)
    parser.add_argument("--mrbc", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path, help="new evidence directory")
    parser.add_argument("--repeat", type=probe.positive_int, default=5)
    args = parser.parse_args()
    source, mrbc, out = args.mrubyc.resolve(), args.mrbc.resolve(), args.out.resolve()
    here = Path(__file__).resolve().parent
    if out.is_relative_to(here.parents[3]) or out.is_relative_to(source) or source.is_relative_to(out):
        parser.error("output must be outside the repository and source tree")
    try:
        expected = read_expected(here / "expected.json")
    except (OSError, ValueError) as error:
        parser.error(str(error))
    if out.exists():
        parser.error("output already exists; select a new --out")
    for tool in ("git", "make", "ruby", "cc", "ar"):
        if not shutil.which(tool):
            parser.error("missing tool: " + tool)
    if not (source / "src/vm_config.h").is_file() or not mrbc.is_file():
        parser.error("invalid source or mrbc")
    out.mkdir(parents=True)
    inputs = [here / name for name in ("binding.c", "value_contract.c", "contract.rb", "run.py", "expected.json")]
    inputs.append(Path(probe.__file__).resolve())
    metadata = {"repeat": args.repeat, "commands": [], "build_flags": probe.CFLAGS,
                "input_sha256": {str(p.relative_to(here)) if p.is_relative_to(here) else "probe_mrubyc.py":
                                 hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}}
    env = dict(os.environ, LC_ALL="C", TZ="UTC")
    for key in ("MAKEFLAGS", "MFLAGS", "CFLAGS", "CPPFLAGS", "LDFLAGS", "MRBC_USE_HAL",
                "MRBC_USE_HAL_POSIX", "MRBC_USE_STRING_UTF8", "MRBC_USE_UNICODE_CASE"):
        env.pop(key, None)

    def save():
        (out / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")

    def checked(label, command):
        result = probe.execute(command, 120, env=env)
        metadata["commands"].append(result)
        (out / (label + ".json")).write_text(json.dumps(result, indent=2) + "\n")
        save()
        if result["timed_out"] or result["exit_code"] != 0:
            raise RuntimeError(label + ": " + probe.first_line(result["stderr"] or result["stdout"]))
        return result["stdout"].strip()

    try:
        metadata["commit"] = checked("git-commit", ["git", "-C", str(source), "rev-parse", "HEAD"])
        metadata["describe"] = checked("git-describe", ["git", "-C", str(source), "describe", "--tags", "--always", "--dirty"])
        status = checked("git-status", ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=all"])
        if status:
            raise RuntimeError("mruby/c source must be clean")
        metadata["mrbc_version"] = checked("mrbc-version", [str(mrbc), "--version"])
        if not metadata["mrbc_version"].startswith("mruby 4.0.0 "):
            raise RuntimeError("mrbc 4.0.0 is required")
        metadata["compiler"] = checked("cc-version", ["cc", "--version"])
        metadata["vm_config_sha256"] = hashlib.sha256((source / "src/vm_config.h").read_bytes()).hexdigest()
        runs = []
        with tempfile.TemporaryDirectory(prefix="binding-contract-") as directory:
            work = Path(directory)
            copied = work / "mrubyc"
            shutil.copytree(source, copied, ignore=shutil.ignore_patterns(".git", "build", "__pycache__"))
            checked("build-mrblib", ["make", "-C", str(copied / "mrblib"), "all", "MRBC=" + str(mrbc)])
            checked("build-autogen", ["make", "-C", str(copied / "src"), "autogen"])
            checked("build-library", ["make", "-C", str(copied / "src"), "CC=" + shutil.which("cc"),
                                      "AR=" + shutil.which("ar"), "ARFLAGS=rcs", "CFLAGS=" + " ".join(probe.CFLAGS)])
            harness = work / "main.c"
            harness.write_text("void binding_contract_init(void);\n" + probe.HARNESS.replace(
                "mrbc_init(pool, sizeof(pool));", "mrbc_init(pool, sizeof(pool));\n  binding_contract_init();"))
            executable = work / "runner"
            checked("build-runner", ["cc", "-Wall", "-Wextra", "-Wno-unused-parameter", "-g", "-O0",
                                     "-I" + str(copied / "src"), "-I" + str(copied / "hal/posix"),
                                     str(harness), str(here / "binding.c"), str(here / "value_contract.c"),
                                     str(copied / "build/libmrubyc.a"), "-lm", "-o", str(executable)])
            metadata["vm_config"] = json.loads(checked("vm-config", [str(executable), "--config"]))
            for index in range(1, args.repeat + 1):
                bytecode = out / ("run-" + str(index) + ".mrb")
                compilation = probe.execute([str(mrbc), "-o", str(bytecode), str(here / "contract.rb")], 10, env=env)
                result = {"compile": compilation}
                if compilation["exit_code"] == 0 and not compilation["timed_out"]:
                    result["run"] = probe.execute([str(executable), str(bytecode)], 3, env=env)
                for phase, evidence in result.items():
                    base = out / ("run-" + str(index) + "." + phase)
                    base.with_suffix(base.suffix + ".json").write_text(json.dumps(evidence, indent=2) + "\n")
                    for stream in ("stdout", "stderr"):
                        base.with_suffix(base.suffix + "." + stream).write_text(evidence[stream])
                runs.append(result)
        rows, identical, passed = evaluate(runs, expected)
        metadata.update(rows=rows, identical=identical, passed=passed, expected_checks=len(expected))
        after = checked("git-status-after", ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=all"])
        if after != status:
            raise RuntimeError("source tree changed")
        save()
        for index, row in enumerate(rows, 1):
            print(f"Run {index}: {row[0]}; exit={row[1]}; {row[2]}")
        print(f"Repeats: {len(rows)}; identical status/exit/diagnostic: {'YES' if identical else 'NO'}")
        print(f"Checks per run: {len(expected) - 1} + completion marker")
        print("Source tree unchanged: YES")
        print("Result: " + ("PASS" if passed else "FAIL"))
        print("Evidence: " + str(out))
        return 0 if passed else 1
    except (OSError, ValueError, RuntimeError) as error:
        metadata["error"] = str(error)
        save()
        print("ERROR: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

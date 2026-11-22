#!/usr/bin/env python3
"""Run isolated Ruby compatibility probes; retain evidence beside the CSV."""

import argparse
import collections
import csv
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time


STATUSES = {"PASS", "FAIL", "COMPILE_ERROR", "RUNTIME_ERROR", "TIMEOUT"}
CFLAGS = ["-Wall", "-g", "-O0", "-I../hal/posix"]
FIELDS = ["id", "status", "exit_code", "diagnostic"]
HARNESS = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "mrubyc.h"

static uint8_t pool[1024 * 1024];

int main(int argc, char **argv) {
  if (argc == 2 && strcmp(argv[1], "--config") == 0) {
    printf("{\"integer_bits\":%zu,\"float_bits\":%zu,"
           "\"memory_pool_bytes\":%zu,\"max_regs\":%d,"
           "\"max_symbols\":%d,\"string_utf8\":%d}\n",
           sizeof(mrbc_int_t) * 8, sizeof(mrbc_float_t) * 8,
           sizeof(pool), MAX_REGS_SIZE, MAX_SYMBOLS_COUNT, MRBC_USE_STRING_UTF8);
    return 0;
  }
  if (argc != 2) return 64;
  FILE *file = fopen(argv[1], "rb");
  if (!file) { perror("fopen"); return 65; }
  if (fseek(file, 0, SEEK_END) != 0) return 65;
  long length = ftell(file);
  if (length <= 0 || fseek(file, 0, SEEK_SET) != 0) return 65;
  unsigned char *code = malloc((size_t)length);
  if (!code) return 66;
  if (fread(code, 1, (size_t)length, file) != (size_t)length) return 65;
  fclose(file);
  mrbc_init(pool, sizeof(pool));
  if (!mrbc_create_task(code, NULL)) { free(code); return 67; }
  int result = mrbc_run();
  free(code);
  return result;
}
'''


def execute(command, timeout, cwd=None, env=None):
    started = time.monotonic()
    try:
        result = subprocess.run(command, cwd=cwd, env=env, timeout=timeout,
                                capture_output=True)
        code, stdout, stderr, timed_out = result.returncode, result.stdout, result.stderr, False
    except subprocess.TimeoutExpired as error:
        code, stdout, stderr, timed_out = None, error.stdout or b"", error.stderr or b"", True
    return {"command": [str(part) for part in command], "cwd": str(cwd) if cwd else None,
            "exit_code": code, "stdout": stdout.decode("utf-8", "replace"),
            "stderr": stderr.decode("utf-8", "replace"), "timed_out": timed_out,
            "seconds": round(time.monotonic() - started, 6)}


def first_line(text):
    return next((line.strip() for line in text.splitlines() if line.strip()), "")


def classify(probe_id, compilation, runtime=None):
    if compilation["timed_out"]:
        return "TIMEOUT", compilation["exit_code"], "compile timeout"
    if compilation["exit_code"] != 0:
        return "COMPILE_ERROR", compilation["exit_code"], first_line(compilation["stderr"] or compilation["stdout"])
    if runtime is None:
        raise ValueError("runtime is required after successful compilation")
    if runtime["timed_out"]:
        return "TIMEOUT", runtime["exit_code"], "runtime timeout"
    output = runtime["stdout"].splitlines()
    failures = [line for line in output if line.startswith("FAIL " + probe_id + " ")]
    if failures:
        return "FAIL", runtime["exit_code"], failures[0]
    if runtime["exit_code"] != 0:
        return "RUNTIME_ERROR", runtime["exit_code"], first_line(runtime["stderr"] or runtime["stdout"]) or "process failed without diagnostic"
    if runtime["stdout"] == "PASS " + probe_id + "\n" and not runtime["stderr"]:
        return "PASS", 0, "PASS " + probe_id
    return "FAIL", 0, first_line(runtime["stderr"] or runtime["stdout"]) or "missing PASS marker"


def read_expected(path, probe_ids):
    if path is None:
        return None
    expected = {}
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if not reader.fieldnames or not {"id", "status"} <= set(reader.fieldnames):
            raise ValueError("expected CSV requires id,status columns")
        for row in reader:
            if row["id"] in expected or row["status"] not in STATUSES:
                raise ValueError("duplicate id or invalid expected status: " + repr(row))
            expected[row["id"]] = row["status"]
    if set(expected) != set(probe_ids):
        raise ValueError("expected CSV ids must exactly match probe ids")
    return expected


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def compare_results(iterations, expected):
    rows = iterations[0]
    unstable = sorted({a["id"] for other in iterations[1:] for a, b in zip(rows, other) if a != b})
    mismatches = [row["id"] for row in rows if expected is not None and expected[row["id"]] != row["status"]]
    return unstable, mismatches


def positive_int(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mrubyc", type=Path, required=True)
    parser.add_argument("--mrbc", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("results.csv"))
    parser.add_argument("--repeat", type=positive_int, default=1)
    parser.add_argument("--expected", type=Path, help="defaults to expected.csv beside this runner, if present")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    probes = sorted((here / "probes").glob("*.rb"))
    if not probes:
        parser.error("no probe fixtures found")
    source = args.mrubyc.resolve()
    mrbc = args.mrbc.resolve()
    out = args.out.resolve()
    metadata_path = out.with_suffix(".metadata.json")
    evidence = out.with_suffix(".runs")
    if any(path.exists() for path in (out, metadata_path, evidence)):
        parser.error("output already exists; select a new --out to preserve earlier evidence")
    expected_path = args.expected
    if expected_path is None and (here / "expected.csv").exists():
        expected_path = here / "expected.csv"
    try:
        expected = read_expected(expected_path, [probe.stem for probe in probes])
    except (OSError, ValueError) as error:
        parser.error(str(error))
    cc = shutil.which("cc")
    for name in ("make", "ruby", "git", "cc", "ar"):
        if not shutil.which(name):
            parser.error("required tool is unavailable: " + name)
    if not mrbc.is_file() or not (source / "src" / "vm_config.h").is_file():
        parser.error("invalid mrbc executable or mrubyc source directory")
    out.parent.mkdir(parents=True, exist_ok=True)
    evidence.mkdir()
    env = dict(os.environ, LC_ALL="C", TZ="UTC")
    for key in ("MAKEFLAGS", "MFLAGS", "CFLAGS", "CPPFLAGS", "LDFLAGS", "MRBC_USE_HAL", "MRBC_USE_HAL_POSIX", "MRBC_USE_STRING_UTF8", "MRBC_USE_UNICODE_CASE"):
        env.pop(key, None)
    metadata = {"schema_version": 1, "platform": platform.platform(),
                "python": sys.version, "source": str(source), "mrbc": str(mrbc),
                "repeat": args.repeat, "compile_timeout_seconds": 10,
                "runtime_timeout_seconds": 3, "build_timeout_seconds": 120,
                "build_flags": CFLAGS, "link_flags": ["-lm"],
                "expected": str(expected_path) if expected_path else None,
                "probe_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in probes},
                "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "commands": []}

    def save():
        metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False) + "\n")

    def checked(label, command, cwd=None):
        result = execute(command, 120, cwd, env)
        metadata["commands"].append(result)
        (evidence / (label + ".json")).write_text(json.dumps(result, indent=2) + "\n")
        save()
        if result["timed_out"] or result["exit_code"] != 0:
            raise RuntimeError(label + ": " + first_line(result["stderr"] or result["stdout"]))
        return result["stdout"].strip()

    try:
        metadata["mrubyc_commit"] = checked("git-commit", ["git", "-C", str(source), "rev-parse", "HEAD"])
        metadata["mrubyc_describe"] = checked("git-describe", ["git", "-C", str(source), "describe", "--tags", "--always", "--dirty"])
        metadata["mrubyc_status"] = checked("git-status", ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=all"])
        if metadata["mrubyc_status"]:
            raise RuntimeError("mrubyc source must be clean for reproducible copying")
        metadata["mrbc_version"] = checked("mrbc-version", [str(mrbc), "--version"])
        if not re.match(r"mruby 4\.0\.0(?:\s|$)", metadata["mrbc_version"]):
            raise RuntimeError("this probe kit requires mrbc 4.0.0")
        metadata["compiler_version"] = checked("cc-version", [cc, "--version"])
        metadata["ruby_version"] = checked("ruby-version", ["ruby", "--version"])
        metadata["make_version"] = checked("make-version", ["make", "--version"])
        metadata["vm_config_sha256"] = hashlib.sha256((source / "src" / "vm_config.h").read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory(prefix="mrubyc-probes-") as directory:
            work = Path(directory)
            copied = work / "mrubyc"
            shutil.copytree(source, copied, ignore=shutil.ignore_patterns(".git", "build", "__pycache__"))
            checked("build-mrblib", ["make", "-C", str(copied / "mrblib"), "all", "MRBC=" + str(mrbc)])
            checked("build-autogen", ["make", "-C", str(copied / "src"), "autogen"])
            checked("build-library", ["make", "-C", str(copied / "src"), "CC=" + cc, "AR=" + shutil.which("ar"), "ARFLAGS=rcs", "CFLAGS=" + " ".join(CFLAGS)])
            harness = work / "runner.c"
            harness.write_text(HARNESS)
            executable = work / "runner"
            checked("build-runner", [cc, "-Wall", "-g", "-O0", "-I" + str(copied / "src"), "-I" + str(copied / "hal" / "posix"), str(harness), str(copied / "build" / "libmrubyc.a"), "-lm", "-o", str(executable)])
            metadata["vm_config"] = json.loads(checked("vm-config", [str(executable), "--config"]))
            iterations = []
            for iteration in range(1, args.repeat + 1):
                run_dir = evidence / ("run-" + str(iteration))
                run_dir.mkdir()
                rows = []
                for probe in probes:
                    bytecode = run_dir / (probe.stem + ".mrb")
                    compilation = execute([str(mrbc), "-o", str(bytecode), str(probe)], 10, env=env)
                    runtime = None
                    if compilation["exit_code"] == 0 and not compilation["timed_out"]:
                        runtime = execute([str(executable), str(bytecode)], 3, env=env)
                    for phase, result in (("compile", compilation), ("run", runtime)):
                        if result is None:
                            continue
                        base = run_dir / (probe.stem + "." + phase)
                        base.with_suffix(base.suffix + ".json").write_text(json.dumps(result, indent=2) + "\n")
                        base.with_suffix(base.suffix + ".stdout").write_text(result["stdout"])
                        base.with_suffix(base.suffix + ".stderr").write_text(result["stderr"])
                    status, code, diagnostic = classify(probe.stem, compilation, runtime)
                    diagnostic = diagnostic.replace(str(work), "<build>").replace(str(run_dir), "<run>")
                    rows.append(dict(id=probe.stem, status=status, exit_code=code, diagnostic=diagnostic))
                write_csv(run_dir / "results.csv", rows)
                iterations.append(rows)
            rows = iterations[0]
            write_csv(out, rows)
            unstable, mismatches = compare_results(iterations, expected)
            metadata.update(status_counts=dict(collections.Counter(row["status"] for row in rows)),
                            identical_repeats=not unstable, unstable_ids=unstable, expected_mismatches=mismatches)
        after = checked("git-status-after", ["git", "-C", str(source), "status", "--porcelain", "--untracked-files=all"])
        if after != metadata["mrubyc_status"]:
            raise RuntimeError("source tree changed during probe run")
        save()
        print("Probes: " + str(len(rows)))
        print("Statuses: " + ", ".join(f"{status}={metadata['status_counts'].get(status, 0)}" for status in sorted(STATUSES)))
        print(f"Repeats: {args.repeat}; identical status/exit/diagnostic: {'YES' if not unstable else 'NO'}")
        print("Expected: " + (f"{len(mismatches)} mismatches" if expected is not None else "not supplied (capability survey)"))
        print("Source tree unchanged: YES")
        print("CSV: " + str(out))
        print("Metadata: " + str(metadata_path))
        print("Raw outputs: " + str(evidence))
        return 1 if unstable or mismatches else 0
    except (OSError, RuntimeError, ValueError) as error:
        metadata["error"] = str(error)
        save()
        print("ERROR: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())

"""Offline parser and completeness controls; HTML fixtures are Koopman's CC BY 4.0 data."""

from contextlib import redirect_stdout, redirect_stderr
import copy
import hashlib
from html import unescape
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch


REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / ".agents/skills/crc-polynomial"
FIXTURES = Path(__file__).with_name("fixtures")
SPEC = importlib.util.spec_from_file_location("fetch_koopman", SKILL / "scripts/fetch_koopman.py")
CRC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CRC)
EXPECTED = {
    "index.html": 388,
    **dict(zip([f"crc{i}.html" for i in range(3, 33)],
               [2, 4, 3, 6, 11, 17, 16, 16, 17, 22, 21, 25, 25, 43,
                16, 17, 17, 20, 19, 22, 19, 31, 23, 26, 26, 25, 25, 31, 32, 48])),
    **dict(zip([f"crc{i}.html" for i in [36, 40, 44, 48, 52, 56, 60, 63, 64]],
               [12, 12, 9, 9, 8, 7, 4, 0, 5])),
    "hd3.html": 219, "hd4.html": 28, "hd5.html": 26, "hd6.html": 25,
    "6sub8.html": 35, "details.html": 0, "notes.html": 0,
}


class KoopmanTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {name: CRC.read_saved(FIXTURES, name) for name in CRC.PAGES}
        cls.retrieved = json.loads((SKILL / "references/sources.json").read_text())["retrieved"]
        cls.files, cls.counts = CRC.generate(cls.sources, cls.retrieved)

    def document(self, name):
        source = self.sources[name].decode("utf-8")
        return CRC.Document(source), source

    def cli(self, *args):
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return CRC.main(list(args))

    def test_all_source_counts_and_reference_bytes(self):
        self.assertEqual(EXPECTED, self.counts)
        for name, value in self.files.items():
            with self.subTest(file=name):
                self.assertEqual(value.encode(), (SKILL / "references" / name).read_bytes())

    def test_best_all_widths_hd_cells_and_provisional_markers(self):
        doc, source = self.document("index.html")
        rows = CRC.best_rows(doc, source)
        self.assertEqual(set(range(3, 33)), {int(row[0]) for row in rows})
        self.assertIn(["10", "HD=4", "501 0x247"], rows)
        self.assertIn(["32", "HD=6", "32738 0x9960034c (**)"], rows)
        self.assertIn(["3", "HD=4", ""], rows)
        self.assertIn(["3", "HD=2", "0x5"], rows)
        self.assertIn("temporary result", self.files["best-crcs.md"])

    def test_prose_boundaries_preserve_words_without_changing_data(self):
        source = ("<P>BER<B>such</B>as<A>Wikipedia</A>for<BR>reference"
                  "<I></I>text &amp; 1/2<SUP>k</SUP>.</P>"
                  "<TABLE><TR><TD>{<B>247</B>,15,6}</TD></TR></TABLE>")
        doc = CRC.Document(source)
        self.assertEqual([("p", "BER such as Wikipedia for reference text & 1/2<sup>k</sup>.", "")],
                         doc.prose_blocks)
        self.assertEqual([[["{247,15,6}"]]], doc.tables)
        self.assertIn("random independent BER such as", self.files["best-crcs.md"])
        self.assertNotIn("BERsuch", self.files["best-crcs.md"])
        self.assertIn("Wikipedia for", self.files["notes.md"])

    def test_all_prose_matches_source_with_tags_replaced_by_spaces(self):
        def spaced(source):
            return CRC.plain(unescape(re.sub(r"<!--.*?-->|<[^>]*>", " ", source, flags=re.S)))

        for name, data in self.sources.items():
            with self.subTest(source=name):
                source = data.decode()
                masked = re.sub(r"<!--.*?-->", lambda m: " " * len(m[0]), source, flags=re.S)
                stack, expected = [], []
                for match in re.finditer(r"<(/?)(p|li|h[123])\b[^>]*>", masked, re.I):
                    tag = match[2].lower()
                    if not match[1]:
                        stack.append((tag, match.start()))
                    else:
                        kind, start = stack.pop()
                        self.assertEqual(kind, tag)
                        expected.append((kind, spaced(source[start:match.end()])))
                self.assertEqual([], stack)
                doc = CRC.Document(source)
                actual = [(kind, CRC.plain(re.sub(r"</?sup>", " ", text)))
                          for kind, text, _ in doc.prose_blocks]
                self.assertEqual(expected, actual)
                if name in ("notes.html", "details.html"):
                    self.assertEqual(spaced(source),
                                     CRC.plain(re.sub(r"</?sup>", " ", "".join(doc.text_parts))))

    def test_zoo_all_forms_attributes_and_brackets(self):
        doc, source = self.document("crc8.html")
        rows = CRC.zoo_rows(doc, source, "crc8.html")
        row = next(row for row in rows if row[1] == "0xa6")
        self.assertEqual(["8", "0xa6", "0x14d", "0xb2", "0x165", "{247,15,6}"], row[:6])
        self.assertIn("[@246:proper,2.7x]", row[6])
        self.assertTrue(any("gold" in row[-1] for row in rows))
        self.assertTrue(any("[@" in row[-1] for row in rows))
        self.assertIn("(*op)", self.files["zoo-03-16.md"])
        self.assertIn("[@246:proper,3.7x]", self.files["zoo-03-16.md"])
        self.assertIn("1/2<sup>k</sup>", self.files["notes.md"])
        self.assertIn("4.2/2<sup>k</sup>", self.files["notes.md"])

    def test_grouped_zoo_heading_not_broken_anchor_determines_width(self):
        doc, source = self.document("crc48.html")
        rows = CRC.zoo_rows(doc, source, "crc48.html")
        self.assertEqual({"45", "46", "47", "48"}, {r[0] for r in rows})

    def test_bare_wide_entries_not_recomputed(self):
        doc, source = self.document("crc56.html")
        rows = CRC.zoo_rows(doc, source, "crc56.html")
        row = next(row for row in rows if row[1] == "0x8A050222800080")
        self.assertEqual(["", "", ""], row[2:5])
        self.assertEqual("{?,?,208787,38395,?,?,439,?,?}", row[5])
        self.assertIn("WD1007-WAH", row[6])
        self.assertIn("0x40000000000003D", [r[1] for r in rows])
        doc, source = self.document("crc52.html")
        row = CRC.zoo_rows(doc, source, "crc52.html")[0]
        self.assertEqual(["49", "0x1000000000038", "", "", "", "{?,34088924,148539}"], row[:6])
        doc, source = self.document("crc60.html")
        self.assertEqual(["60", "61", "62", "63"],
                         [r[0] for r in CRC.zoo_rows(doc, source, "crc60.html")])

    def test_empty_published_crc63_and_unknown_64_lengths(self):
        doc, source = self.document("crc63.html")
        self.assertEqual([], CRC.zoo_rows(doc, source, "crc63.html"))
        self.assertIn("????HD=11?????", self.files["zoo-33-64.md"])

    def test_each_selection_type_and_published_anomalies_preserved(self):
        for name in CRC.SELECTION:
            with self.subTest(source=name):
                doc, source = self.document(name)
                rows = CRC.selection_rows(doc, source, name)
                self.assertEqual(EXPECTED[name], len(rows))
                self.assertEqual(len(rows), CRC.raw_count(source, "selection"))
                for anomaly in CRC.PUBLISHED_ANOMALIES.get(name, set()):
                    self.assertTrue(any(anomaly in row for row in rows), anomaly)

    def test_deterministic_with_different_source_insertion_order(self):
        files, _ = CRC.generate(dict(reversed(list(self.sources.items()))), self.retrieved)
        self.assertEqual(self.files, files)

    def test_attribution_date_modification_and_row_citations(self):
        for name, value in self.files.items():
            if not name.endswith(".md"):
                continue
            with self.subTest(file=name):
                self.assertIn(CRC.NOTICE, value)
                self.assertIn("Retrieved: " + self.retrieved, value)
                self.assertIn("Modification:", value)
                for line in value.splitlines():
                    if line.startswith("| ") and not line.startswith(("| ---", "| CRC", "| Anomalous")):
                        self.assertIn(CRC.BASE, line)

    def test_malformed_zoo_entry_rejected(self):
        _, source = self.document("crc3.html")
        source = source.replace("0x9)", "0xGG)", 1)
        with self.assertRaisesRegex(ValueError, "malformed Zoo"):
            CRC.zoo_rows(CRC.Document(source), source, "crc3.html")

    def test_bare_bad_hex_and_unclosed_lengths_rejected(self):
        for value in ("0x12GG", "0x12 {1,2"):
            source = f"<H1>CRC Polynomial Zoo</H1><P>{value}</P>"
            with self.subTest(value=value), self.assertRaises(ValueError):
                CRC.zoo_rows(CRC.Document(source), source, "crc52.html")

    def test_dropped_entry_count_mismatch_rejected(self):
        doc, source = self.document("crc3.html")
        doc.blocks = [b for b in doc.blocks if "CRC-3K" not in b[1]]
        with self.assertRaisesRegex(ValueError, "count mismatch"):
            CRC.zoo_rows(doc, source, "crc3.html")

    def test_bad_selection_not_accepted_as_known_anomaly(self):
        doc, source = self.document("hd3.html")
        for table in doc.tables:
            for row in table:
                if "(0x5b3ca4; xb67949)" in row:
                    row[row.index("(0x5b3ca4; xb67949)")] = "(0x5b3ca4; xb67948)"
        with self.assertRaisesRegex(ValueError, "malformed polynomial"):
            CRC.selection_rows(doc, source, "hd3.html")

    def test_missing_best_width_or_hd_rejected(self):
        original, source = self.document("index.html")
        for change in ("width", "hd"):
            doc = copy.deepcopy(original)
            if change == "width":
                doc.tables[0][1][0] = "4"
            else:
                doc.tables[0].pop(3)
            with self.subTest(change=change), self.assertRaises(ValueError):
                CRC.best_rows(doc, source)

    def test_malformed_and_empty_documents_rejected(self):
        for source in ("<TABLE><TR><TD>x</TR></TABLE>", "<P>x"):
            with self.subTest(source=source), self.assertRaises(ValueError):
                CRC.Document(source)
        with self.assertRaises(ValueError):
            CRC.selection_rows(CRC.Document(""), "", "hd3.html")
        with self.assertRaises(ValueError):
            CRC.zoo_rows(CRC.Document(""), "", "crc3.html")
        with self.assertRaises(ValueError):
            CRC.zoo_rows(CRC.Document("<H1>404</H1>"), "<H1>404</H1>", "crc63.html")

    def test_missing_source_and_invalid_date_rejected(self):
        sources = dict(self.sources)
        sources.pop("crc3.html")
        for data, day in [(sources, self.retrieved), (self.sources, "invalid")]:
            with self.assertRaises(ValueError):
                CRC.generate(data, day)

    def test_new_details_polynomial_fails_closed(self):
        sources = dict(self.sources)
        sources["details.html"] += b"<P>0x123</P>"
        with self.assertRaisesRegex(ValueError, "now contains polynomials"):
            CRC.generate(sources, self.retrieved)

    def test_cli_offline_check_and_mismatch_do_not_fetch_or_write(self):
        with patch.object(CRC, "urlopen", side_effect=AssertionError("network in offline check")):
            self.assertEqual(0, self.cli("--html-dir", str(FIXTURES), "--check"))
            with tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                for name, content in self.files.items():
                    (root / name).write_text(content)
                (root / "best-crcs.md").write_text("tampered")
                self.assertEqual(1, self.cli("--html-dir", str(FIXTURES), "--check", "--output", directory))
                self.assertEqual("tampered", (root / "best-crcs.md").read_text())
                (root / "unexpected.md").write_text("extra")
                self.assertEqual(1, self.cli("--html-dir", str(FIXTURES), "--check", "--output", directory))
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(1, self.cli("--html-dir", directory, "--check"))

    def test_cli_generation_and_network_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            args = ["--output", directory, "--retrieved", self.retrieved]
            self.assertEqual(0, self.cli("--html-dir", str(FIXTURES), *args))
            before = {p.name: p.read_bytes() for p in Path(directory).iterdir()}
            self.assertEqual({n: v.encode() for n, v in self.files.items()}, before)
            with patch.object(CRC, "urlopen", side_effect=OSError("offline")):
                self.assertEqual(1, self.cli(*args))
            self.assertEqual(before, {p.name: p.read_bytes() for p in Path(directory).iterdir()})

    def test_saved_html_zstd_preserves_bytes_and_ambiguous_input_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.assertEqual(0, self.cli("--html-dir", str(FIXTURES), "--output", str(root / "refs"),
                                         "--save-html-dir", directory, "--retrieved", self.retrieved))
            for name, value in self.sources.items():
                self.assertEqual(value, CRC.read_saved(root, name))
            (root / "crc3.html").write_bytes(self.sources["crc3.html"])
            with self.assertRaisesRegex(ValueError, "Ambiguous"):
                CRC.read_saved(root, "crc3.html")
            (root / "crc3.html.zst").unlink()
            self.assertEqual(self.sources["crc3.html"], CRC.read_saved(root, "crc3.html"))
            with self.assertRaises(SystemExit), redirect_stderr(io.StringIO()):
                CRC.main(["--check", "--save-html-dir", directory])

    def test_zstd_level22_determinism_and_committed_hashes(self):
        manifest = json.loads((FIXTURES / "compression.json").read_text())
        self.assertEqual("zstd", manifest["format"])
        self.assertEqual(22, manifest["options"]["compression_level"])
        self.assertEqual(27, manifest["options"]["window_log"])
        self.assertEqual(CRC.ZSTD_OPTIONS, manifest["options"])
        source_manifest = json.loads(self.files["sources.json"])["sources"]
        for name, data in self.sources.items():
            with self.subTest(source=name):
                compressed = (FIXTURES / (name + ".zst")).read_bytes()
                self.assertEqual(source_manifest[name]["sha256"], hashlib.sha256(data).hexdigest())
                self.assertEqual(manifest["files"][name + ".zst"], hashlib.sha256(compressed).hexdigest())
                self.assertEqual(CRC.compress_saved(data), CRC.compress_saved(data))
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            CRC.save_snapshots(root, self.sources)
            before = (root / "compression.json").read_bytes()
            CRC.save_snapshots(root, dict(reversed(list(self.sources.items()))))
            self.assertEqual(before, (root / "compression.json").read_bytes())

    def test_missing_zstd_and_corrupt_snapshot_fail_clearly(self):
        with patch.object(CRC, "zstd", None), redirect_stderr(io.StringIO()) as stderr:
            self.assertEqual(1, CRC.main(["--check"]))
            self.assertIn("compression.zstdを備えたPython 3.14以降が必要です", stderr.getvalue())
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "crc3.html.zst").write_bytes(b"not a zstd frame")
            with self.assertRaisesRegex(ValueError, "zstd展開に失敗"):
                CRC.read_saved(Path(directory), "crc3.html")


if __name__ == "__main__":
    unittest.main()

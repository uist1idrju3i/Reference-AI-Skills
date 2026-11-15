"""Fetch Koopman's tables, preserving published values without computing CRCs."""

import argparse
from datetime import date
import gzip
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from urllib.request import urlopen


BASE = "https://users.ece.cmu.edu/~koopman/crc/"
ZOO = [f"crc{i}.html" for i in [*range(3, 33), 36, 40, 44, 48, 52, 56, 60, 63, 64]]
SELECTION = [f"hd{i}.html" for i in range(3, 7)] + ["6sub8.html"]
PAGES = ["index.html", *ZOO, *SELECTION, "details.html", "notes.html"]
HEX = r"0x[0-9a-fA-F]+"
FORMS = re.compile(rf"\(({HEX});\s*({HEX})\)\s*<=>\s*\(({HEX});\s*({HEX})\)\s*(\{{[^{{}}]*\}})(.*)")
NOTICE = "Copyright 2015-2018 Philip Koopman, Carnegie Mellon University, CC BY 4.0 (http://creativecommons.org/licenses/by/4.0/)"
ROOT = Path(__file__).resolve().parents[1]
PUBLISHED_ANOMALIES = {
    "hd3.html": {
        "(0x5b3ca4; xb67949)", "(0x306fe75; 0x60dfceb",
        "0xbd07453; 0x17a0e8a7)", ".(0x81620e5; 0x102c41cb)",
        "(0x16dfbf51; 0x2dbf7ea3))", "(0x31342a2f; 0x6268545f))",
        "(0x4a3ed66b; 0x947dacd7",
    },
    "hd4.html": {"16777190,16777190,1059,1059,38,38,8,8,6,6,2,2}"},
    "hd5.html": {"0(0x74f9e7cb; 0xe9f3cf97)"},
    "6sub8.html": {"(0x200e7; 0x401cf", "(0x200053; 0x4000a7", "(0x800004d; 0x1000009b"},
}


def plain(value):
    return " ".join(value.split())


def read_saved(directory, name):
    html, compressed = directory / name, directory / (name + ".gz")
    if html.exists() and compressed.exists():
        raise ValueError(f"Ambiguous saved HTML: {name}")
    return html.read_bytes() if html.exists() else gzip.decompress(compressed.read_bytes())


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tables = []
        self.table = None
        self.row = None
        self.cell = None
        self.blocks = []
        self.prose_blocks = []
        self.active = []
        self.prose_active = []
        self.text_parts = []
        self.width = ""
        self.feed(source)
        self.close()
        if self.table is not None or self.active:
            raise ValueError("Unclosed table or text block")

    def handle_starttag(self, tag, attrs):
        if tag != "sup":
            self.prose_boundary()
        if tag == "table":
            if self.table is not None:
                raise ValueError("Nested table")
            self.table = []
        elif tag == "tr":
            if self.table is None or self.row is not None:
                raise ValueError("Malformed table row")
            self.row = []
        elif tag in ("td", "th"):
            if self.row is None or self.cell is not None:
                raise ValueError("Malformed table cell")
            self.cell = []
        elif tag in ("p", "li", "h1", "h2", "h3"):
            self.active.append((tag, [], self.width))
            self.prose_active.append([])
        elif tag == "br":
            self.handle_data(" ")
        elif tag == "sup":
            self.handle_data("<sup>")

    def handle_data(self, data):
        self.text_parts.append(data)
        for parts in self.prose_active:
            parts.append(data)
        if self.cell is not None:
            self.cell.append(data)
        for _, parts, _ in self.active:
            parts.append(data)

    def prose_boundary(self):
        self.text_parts.append(" ")
        for parts in self.prose_active:
            parts.append(" ")

    def handle_endtag(self, tag):
        if tag == "sup":
            self.handle_data("</sup>")
        elif tag in ("td", "th"):
            if self.cell is None:
                raise ValueError("Unexpected cell end")
            self.row.append(plain("".join(self.cell)))
            self.cell = None
        elif tag == "tr":
            if self.row is None or self.cell is not None:
                raise ValueError("Unclosed cell")
            self.table.append(self.row)
            self.row = None
        elif tag == "table":
            if self.table is None or self.row is not None:
                raise ValueError("Unclosed row")
            self.tables.append(self.table)
            self.table = None
        elif tag in ("p", "li", "h1", "h2", "h3"):
            if not self.active or self.active[-1][0] != tag:
                raise ValueError(f"Malformed {tag} block")
            kind, parts, width = self.active.pop()
            value = plain("".join(parts))
            self.blocks.append((kind, value, width))
            prose = plain("".join(self.prose_active.pop()))
            self.prose_blocks.append((kind, prose, width))
            match = re.match(r"(\d+)\s*-?\s*Bit CRCs", value, re.I)
            if kind in ("h2", "h3") and match:
                self.width = match[1]
        if tag != "sup":
            self.prose_boundary()


def raw_count(source, kind):
    """Count source markers separately from the structured parser."""
    if kind == "zoo":
        full = len(re.findall(r"<LI>\s*<TT>\s*\(", source, re.I))
        bare = 0
        for block in re.findall(r"<P\b[^>]*>(.*?)</P>", source, re.I | re.S):
            value = plain(unescape(re.sub(r"<[^>]+>", "", block)))
            bare += bool(re.match(r"(?:\d+:\s*)?0x", value))
        return full + bare
    if kind == "selection":
        return len(re.findall(r"<TD\b[^>]*>\s*(?:[.0]?\()?\s*(?:<A\b[^>]*>)?0x", source, re.I))
    return sum(len(re.findall(r"<TD\b[^>]*>", row, re.I)) - 1
               for row in re.findall(r"<TR\b[^>]*>(.*?)</TR>", source, re.I | re.S)
               if re.search(r"HD=\d+", re.sub(r"<[^>]+>", "", row)))


def expect_count(actual, expected, location):
    if actual != expected:
        raise ValueError(f"{location}: count mismatch: parsed {actual}, raw/expected {expected}")


def zoo_rows(document, source, name):
    if not any(kind == "h1" and value == "CRC Polynomial Zoo" for kind, value, _ in document.blocks):
        raise ValueError(f"{name}: not a CRC Zoo page")
    rows = []
    for kind, value, width in document.blocks:
        if kind not in ("li", "p") or not re.match(r"(?:\d+:\s*)?\(?0x", value):
            continue
        if value.startswith("("):
            match = FORMS.fullmatch(value)
            if not match:
                raise ValueError(f"{name}: malformed Zoo entry: {value}")
            row = [width, *match.groups()[:5], match[6]]
        else:
            prefix = re.match(r"(\d+):", value)
            match = re.fullmatch(rf"(?:\d+:\s*)?({HEX})(.*)", value)
            if not match:
                raise ValueError(f"{name}: malformed bare entry: {value}")
            remainder = match[2].strip()
            if remainder and not remainder.startswith(("{", "(")):
                raise ValueError(f"{name}: malformed bare entry: {value}")
            lengths = re.search(r"\{[^{}]*\}", remainder)
            if "{" in remainder and lengths is None:
                raise ValueError(f"{name}: malformed bare HD list: {value}")
            named_width = re.search(r"(?:FP-|FOP-)(\d+)", value)
            row = [prefix[1] if prefix else (named_width[1] if named_width else width),
                   match[1], "", "", "", lengths[0] if lengths else "",
                   remainder.replace(lengths[0], "", 1) if lengths else remainder]
        rows.append(row)
    expect_count(len(rows), raw_count(source, "zoo"), name)
    if not rows and name != "crc63.html":
        raise ValueError(f"{name}: empty Zoo")
    return rows


def selection_rows(document, source, name):
    expected_columns = 6 if name in ("hd3.html", "hd4.html", "hd5.html") else 5
    rows = []
    for table in document.tables:
        for row in table[1:]:
            if not any(row):
                continue
            if len(row) != expected_columns or not row[0].isdigit():
                raise ValueError(f"{name}: malformed selection row: {row}")
            poly = row[-3]
            anomalies = PUBLISHED_ANOMALIES.get(name, set())
            if not re.fullmatch(rf"\({HEX};\s*{HEX}\)", poly) and poly not in anomalies:
                raise ValueError(f"{name}: malformed polynomial: {poly}")
            if not re.fullmatch(r"\{[^{}]*\}", row[-1]) and row[-1] not in anomalies:
                raise ValueError(f"{name}: malformed HD list: {row[-1]}")
            rows.append(row)
    expect_count(len(rows), raw_count(source, "selection"), name)
    if not rows:
        raise ValueError(f"{name}: empty selection")
    return rows


def best_rows(document, source):
    rows = []
    widths = []
    for table in document.tables:
        if len(table) < 3 or not all(c.isdigit() for c in table[1]):
            raise ValueError("index.html: malformed width header")
        bits = table[1]
        widths.extend(bits)
        hds = []
        for row in table[2:]:
            if len(row) != len(bits) + 1 or not re.fullmatch(r"HD=\d+", row[0]):
                raise ValueError("index.html: malformed HD row")
            hds.append(int(row[0][3:]))
            for width, value in zip(bits, row[1:]):
                if value and not re.fullmatch(rf"(?:\d+\s+)?{HEX}(?:\s*\(\*\*\))?", value):
                    raise ValueError(f"index.html: malformed value: {value}")
                rows.append([width, row[0], value])
        if hds != list(range(2, max(hds) + 1)):
            raise ValueError("index.html: missing or duplicate HD row")
    if widths != [str(i) for i in range(3, 33)]:
        raise ValueError("index.html: missing or duplicate CRC width")
    expect_count(len(rows), raw_count(source, "best"), "index.html HD cells")
    return rows


def markdown_table(headers, rows, url):
    def escape(value):
        return (value or "—").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("|", "\\|")
    return "\n".join([
        "| " + " | ".join([*headers, "Source"]) + " |",
        "| " + " | ".join(["---"] * (len(headers) + 1)) + " |",
        *("| " + " | ".join([*(escape(c) for c in row), url]) + " |" for row in rows),
    ]) + "\n"


def header(title, names, retrieved, documents):
    notices = []
    for name in names:
        for kind, value, _ in documents[name].prose_blocks:
            if kind == "p" and "copyright" in value.lower():
                notices.append(f"> {name}: {value}")
    return (f"# {title}\n\n" + "\n".join(f"Source: {BASE + n}" for n in names)
            + f"\n\nRetrieved: {retrieved}\n\n{NOTICE}\n\n"
            + "Modification: HTML was reformatted into Markdown tables; layout whitespace and visual styling were normalized. Values were not calculated or completed. — means not supplied in the source.\n\n"
            + "\n".join(notices) + "\n\n")


def generate(sources, retrieved):
    date.fromisoformat(retrieved)
    if set(sources) != set(PAGES):
        raise ValueError("Missing or unexpected source pages")
    documents = {name: Document(source.decode("utf-8")) for name, source in sources.items()}
    for name, document in documents.items():
        expected = ("Best CRC Polynomials" if name == "index.html" else
                    "Detailed Best CRC Polynomial Selection" if name == "details.html" else
                    "CRC Polynomial Selection" if name in SELECTION else "CRC Polynomial Zoo")
        if not any(kind == "h1" and value == expected for kind, value, _ in document.blocks):
            raise ValueError(f"{name}: unexpected page identity")
    files = {}
    counts = {}
    doc = documents["index.html"]
    rows = best_rows(doc, sources["index.html"].decode("utf-8"))
    counts["index.html"] = len(rows)
    body = header("Best CRCs: all HD cells, 3–32 bits", ["index.html"], retrieved, documents)
    body += "HD=2 cells publish only a polynomial, not a maximum length. Empty cells remain —; no missing value is inferred. Lengths are dataword bits, not codeword bits.\n\n"
    body += markdown_table(["CRC bits", "HD", "Maximum dataword length / implicit +1 polynomial / marker"], rows, BASE + "index.html")
    for kind, value, _ in doc.prose_blocks:
        if (kind == "p" and ("(**)" in value or "minimum dataword" in value.lower() or "assumption" in value)
                or kind == "li" and value.startswith(("*p -", "*o -", "*op -", "** -"))):
            body += "\n> " + value + "\n"
    files["best-crcs.md"] = body
    for title, names in [("zoo-03-16", ZOO[:14]), ("zoo-17-32", ZOO[14:30]), ("zoo-33-64", ZOO[30:])]:
        body = header(title, names, retrieved, documents)
        body += "The attributes column preserves bracket information, gold, names, uncertainty markers, and incomplete bare entries. Bold/color emphasis is not reproduced. Missing forms are not derived. A page label is not a guarantee of width coverage.\n\n"
        for name in names:
            rows = zoo_rows(documents[name], sources[name].decode("utf-8"), name)
            counts[name] = len(rows)
            body += f"## {name}: {len(rows)} entries\n\n"
            body += markdown_table(["CRC bits as stated", "Implicit +1", "Explicit +1", "Reversed implicit +1", "Reversed explicit +1", "HD lengths", "Attributes / names / remaining source text"], rows, BASE + name) + "\n"
            if not rows:
                body += f"No polynomial entries are published on this page: {BASE + name}\n\n"
        files[title + ".md"] = body
    for name in SELECTION:
        rows = selection_rows(documents[name], sources[name].decode("utf-8"), name)
        counts[name] = len(rows)
        headers = ["CRC bits", "Primary HD length"]
        if name in ("hd3.html", "hd4.html", "hd5.html"):
            headers.append("Secondary property")
        headers += ["Polynomial (implicit; explicit)", "Nickname / attributes", "HD lengths"]
        body = header("Selection: " + name, [name], retrieved, documents)
        for kind, value, _ in documents[name].prose_blocks:
            if kind in ("li", "p") and "copyright" not in value.lower() and "licensed" not in value.lower() and "updated" not in value.lower():
                body += "> " + value + "\n\n"
        anomalies = [[cell] for row in rows for cell in row if cell in PUBLISHED_ANOMALIES.get(name, set())]
        if anomalies:
            body += "## Published source anomalies (verbatim; do not use as implementation parameters without verification)\n\n"
            body += markdown_table(["Anomalous cell"], anomalies, BASE + name) + "\n"
        files["selection-" + name[:-5] + ".md"] = body + markdown_table(headers, rows, BASE + name)
    for name in ("details.html", "notes.html"):
        body = header("Selection and notation: " + name, [name], retrieved, documents)
        if name == "details.html" and "0x" in sources[name].decode("utf-8"):
            raise ValueError("details.html now contains polynomials; update its parser before proceeding")
        body += "> " + plain("".join(documents[name].text_parts)) + "\n"
        counts[name] = 0
        files[name[:-5] + ".md"] = body
    manifest = {"copyright": NOTICE, "modification": "HTML reformatted; no values computed.",
                "retrieved": retrieved, "sources": {
        name: {"url": BASE + name, "sha256": hashlib.sha256(sources[name]).hexdigest(),
               "entries": counts[name], "raw_entries": raw_count(sources[name].decode("utf-8"),
               "zoo" if name in ZOO else "selection" if name in SELECTION else "best")
               if name in ZOO + SELECTION + ["index.html"] else 0}
        for name in PAGES}}
    files["sources.json"] = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    return {name: content.rstrip() + "\n" for name, content in files.items()}, counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html-dir", type=Path, help="Read saved HTML instead of using the network")
    parser.add_argument("--output", type=Path, default=ROOT / "references")
    parser.add_argument("--save-html-dir", type=Path, help="Also save byte-preserving gzip HTML snapshots")
    parser.add_argument("--retrieved", help="Retrieval date YYYY-MM-DD; check defaults to the committed date")
    parser.add_argument("--check", action="store_true", help="Compare without writing")
    args = parser.parse_args(argv)
    if args.check and args.save_html_dir:
        parser.error("--check cannot write HTML snapshots")
    try:
        retrieved = args.retrieved or (json.loads((args.output / "sources.json").read_text())["retrieved"]
                                        if args.check else date.today().isoformat())
        sources = {}
        for name in PAGES:
            if args.html_dir:
                sources[name] = read_saved(args.html_dir, name)
            else:
                with urlopen(BASE + name, timeout=45) as response:
                    sources[name] = response.read()
        files, counts = generate(sources, retrieved)
        manifest = json.loads(files["sources.json"])
        for name, count in counts.items():
            print(f"{name}: raw={manifest['sources'][name]['raw_entries']}, parsed={count}")
        if args.check:
            actual = {p.name for p in args.output.iterdir() if p.is_file()}
            if actual != set(files):
                raise ValueError("Reference file set mismatch")
            for name, value in files.items():
                if (args.output / name).read_bytes() != value.encode("utf-8"):
                    raise ValueError(f"Reference mismatch: {name}")
            print(f"Exact match: {len(files)} reference files, {sum(counts.values())} table entries")
        else:
            if args.save_html_dir:
                args.save_html_dir.mkdir(parents=True, exist_ok=True)
                for name, value in sources.items():
                    (args.save_html_dir / (name + ".gz")).write_bytes(gzip.compress(value, mtime=0))
            args.output.mkdir(parents=True, exist_ok=True)
            for name, value in files.items():
                (args.output / name).write_text(value, encoding="utf-8")
            print(f"Generated {len(files)} reference files")
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"CRC data error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

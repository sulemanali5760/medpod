"""Parse WHO electronic EDL (edl.who-healthtechnologies.org) recommendation pages into a CSV.

Usage:
    python3 -I tools/who_edl.py <dir with <id>.html pages> <out.csv>

The pages are fetched separately (curl, one per id listed on the site's home page) and kept
outside the repo; this script only reads them. Text is copied verbatim (tags stripped,
whitespace collapsed). No field is guessed: a missing field is left empty.
"""
import csv
import html
import re
import sys
from pathlib import Path

FIELDS = ["edl_id", "test", "category", "setting", "tiered_testing_service", "assay_format",
          "purpose_type", "purpose", "specimen_types", "first_added", "who_pq_products",
          "sage_section", "url"]


def _text(fragment):
    fragment = re.sub(r"(?s)<script.*?</script>|<style.*?</style>|<svg.*?</svg>", "", fragment)
    fragment = re.sub(r"<br\s*/?>|</p>|</div>", " ", fragment)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", fragment))).strip()


def _row(page, label):
    """Content cell that follows <div class="label-cell">label</div>."""
    m = re.search(r'class="label-cell">\s*' + re.escape(label) +
                  r'\s*</div>\s*<div class="content-cell">(.*?)</div></div>\s*</div>', page, re.S)
    return _text(m.group(1)) if m else ""


def parse(page, edl_id):
    title = re.search(r'<div class="device-title[^"]*" title="([^"]*)"', page)
    cat = re.search(r'<div class="indication-text">(.*?)</div>\s*</div>', page, re.S)
    setting = re.findall(r'href="/\?section\[\]=\d+">\s*<span>(.*?)</span>', page, re.S)
    tiers = re.findall(r'href="/\?tieredTestingService\[\]=\d+">\s*<span>(.*?)</span>', page, re.S)
    added = re.search(r"First added in (\d{4})", page)
    # First line of the SAGE IVD recommendation names the EDL edition and section,
    # e.g. "(EDL 4, Section I.a)". Keep every edition/section reference found.
    sage = re.search(r'id="who-recommendation".*?<div class="recommendation-card">(.*?)</div>', page, re.S)
    sections = re.findall(r"\(EDL \d[^)]*\)", _text(sage.group(1))) if sage else []
    return {
        "edl_id": edl_id,
        "test": html.unescape(title.group(1)).strip() if title else "",
        "category": _text(cat.group(1)) if cat else "",
        "setting": "; ".join(_text(s) for s in setting),
        "tiered_testing_service": "; ".join(_text(t) for t in tiers),
        "assay_format": _row(page, "Assay format"),
        "purpose_type": _row(page, "Purpose type"),
        "purpose": _row(page, "Purpose"),
        "specimen_types": _row(page, "Specimen types"),
        "first_added": added.group(1) if added else "",
        "who_pq_products": _row(page, "WHO prequalified or recommended products"),
        "sage_section": "; ".join(dict.fromkeys(sections)),
        "url": f"https://edl.who-healthtechnologies.org/recommendations/{edl_id}",
    }


def main(src, out):
    pages = sorted(Path(src).glob("*.html"), key=lambda p: int(p.stem))
    if not pages:
        sys.exit(f"no pages in {src}")
    rows = [parse(p.read_text(encoding="utf-8"), int(p.stem)) for p in pages]
    bad = [r["edl_id"] for r in rows if not (r["test"] and r["setting"] and r["assay_format"])]
    if bad:  # never write a silently incomplete list
        sys.exit(f"pages missing title/setting/assay format: {bad}")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} recommendations -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])

"""Phase 2b: cost per test (data/test_costs.csv, tools/test_costs.py)."""
import re

import pytest

from tools.test_costs import PANEL, load, low_high, stages

ROWS = load()


def numbers(text):
    return {float(n) for n in re.findall(r"\d+(?:\.\d+)?", text.replace("·", "."))}


@pytest.mark.parametrize("r", ROWS.values(), ids=lambda r: r["id"])
def test_every_number_is_in_its_quote(r):
    # Transcription check: each price we store must appear verbatim in the quoted source text.
    found = numbers(r["quote"])
    for f in ("low_usd", "high_usd", "point_usd"):
        if r[f]:
            assert float(r[f]) in found, (r["id"], f, r[f], r["quote"])
    assert r["source"] and r["where"] and r["year"] and r["basis"]


@pytest.mark.parametrize("r", ROWS.values(), ids=lambda r: r["id"])
def test_ranges_are_ordered(r):
    vals = [float(r[f]) for f in ("low_usd", "point_usd", "high_usd") if r[f]]
    assert vals == sorted(vals), r["id"]


def test_missing_price_is_never_zero():
    assert not (ROWS["C-12"]["low_usd"] or ROWS["C-12"]["point_usd"])
    with pytest.raises(ValueError):
        low_high(ROWS["C-12"])


def test_d008_set_has_a_cost_row():
    # D-008 cartridge set by EDL 5 id: malaria 34, dual HIV/syphilis 38, HBsAg 20, anti-HCV 22,
    # glucose 4, HbA1c 19, cholesterol 227.
    priced = {i for r in ROWS.values() if r["id"].startswith("C-") for i in r["edl5_ids"].split(";") if i}
    assert {"34", "38", "20", "22", "4", "19", "227"} <= priced
    used = {i for _, ids in PANEL for i in ids}
    assert used <= set(ROWS)


def test_panel_totals_match_hand_sum():
    # Independent hand sums from the quoted values (USD per person):
    # RDTs  low  0.323 + 0.95 + 0.09 + 0.21 + 0.01 = 1.583
    #       high 0.718 + 1.31 + 2.40 + 2.42 + 0.17 = 7.018
    # strip      0.06 / 0.88  -> 1.643 / 7.898
    # HbA1c      6.52         -> 8.163 / 14.418
    # cholesterol 8.57        -> 16.733 / 22.988
    expected = [(1.583, 7.018), (1.643, 7.898), (8.163, 14.418), (16.733, 22.988)]
    got = [v for _, lo, hi in stages(ROWS) for v in (lo, hi)]
    assert got == pytest.approx([v for pair in expected for v in pair], abs=1e-9)

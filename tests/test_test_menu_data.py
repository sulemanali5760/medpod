"""Phase 2 data checks: WHO EDL 4 Tier I transcription, e-EDL (EDL 5) scrape, GHE 2021 top-10 table,
and the test menu that joins them (docs/04-test-menu.md, data/test_menu.csv).

The EDL 4 rows were transcribed by hand from WHO TRS 1053 (PDF); the EDL 5 rows were scraped by
tools/who_edl.py from the e-EDL website. Two official sources, two methods: each EDL 4 row that
names an EDL 5 id must agree with that scraped row on test identity and specimen.
"""
import csv
import re
from pathlib import Path

import pytest

from tools.who_edl import parse

DATA = Path(__file__).resolve().parent.parent / "data"


def rows(name):
    with open(DATA / name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


EDL5 = {int(r["edl_id"]): r for r in rows("who_edl5.csv")}
EDL4 = rows("who_edl4_tier1.csv")
GHE = rows("who_ghe2021_top10_deaths.csv")
MENU = rows("test_menu.csv")


def words(s):
    stop = {"and", "or", "of", "to", "the", "test", "testing", "antigen", "antibodies", "antibody",
            "spp", "e", "g", "a", "b", "self", "hiv", "1", "2"}
    return {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in stop and len(w) > 1}


SPECIMEN_WORDS = {"capillary", "venous", "urine", "stool", "rectal", "oral", "plasma", "serum",
                  "throat", "nasal", "nasopharyngeal", "respiratory", "dried"}


def test_edl5_scrape_complete():
    # e-EDL home page listed ids 1..234 on 2026-11-02; every one parsed with core fields.
    assert sorted(EDL5) == list(range(1, 235))
    for r in EDL5.values():
        assert r["test"] and r["setting"] and r["assay_format"] and r["specimen_types"]
    settings = {r["setting"] for r in EDL5.values()}
    assert settings == {"1. Non-laboratory", "2. Laboratory"}
    assert sum(r["setting"] == "1. Non-laboratory" for r in EDL5.values()) == 39


def test_edl4_tier1_transcription_shape():
    assert len(EDL4) == 39
    assert [int(r["row"]) for r in EDL4] == list(range(1, 40))
    assert {r["section"] for r in EDL4} == {"I.a", "I.b"}
    assert sum(r["section"] == "I.a" for r in EDL4) == 11


@pytest.mark.parametrize("r", EDL4, ids=lambda r: r["row"])
def test_edl4_row_agrees_with_edl5(r):
    ids = [int(i) for i in r["edl5_ids"].split(";") if i]
    if not ids:
        assert r["edl5_note"].startswith("Not found in e-EDL")
        return
    for i in ids:
        e = EDL5[i]
        # Same test: share a meaningful word in the test name (abbreviation or full name),
        # unless the row declares that EDL 5 renamed it.
        if "renamed" in r["edl5_note"]:
            assert e["test"] in r["edl5_note"]
        else:
            assert words(r["ivd_test"]) & words(e["test"]), (r["ivd_test"], e["test"])
        # Same specimen family, unless the row declares that EDL 5 changed it.
        s4 = words(r["specimen_types"]) & SPECIMEN_WORDS
        s5 = words(e["specimen_types"]) & SPECIMEN_WORDS
        if "specimen changed" in r["edl5_note"]:
            assert not s4 & s5 and e["specimen_types"] in r["edl5_note"]
        else:
            assert s4 & s5, (r["specimen_types"], e["specimen_types"])
    # A row moved out of the non-laboratory setting must say so.
    moved = [i for i in ids if EDL5[i]["setting"] != "1. Non-laboratory"]
    if len(moved) == len(ids):
        assert "Laboratory" in r["edl5_note"]


def test_ghe_top10_well_formed():
    groups = {}
    for r in GHE:
        groups.setdefault(r["income_group"], []).append(int(r["rank_2021"]))
    assert set(groups) == {"Low-income", "Lower-middle-income"}
    for ranks in groups.values():
        assert sorted(ranks) == list(range(1, 11))
    for g in groups:
        causes = [r["cause"] for r in GHE if r["income_group"] == g]
        assert len(set(causes)) == 10


def test_menu_references_exist():
    causes = {r["cause"] for r in GHE}
    assert MENU
    for m in MENU:
        for c in filter(None, m["ghe2021_cause"].split(";")):
            assert c in causes, c
        for i in filter(None, m["edl5_ids"].split(";")):
            assert EDL5[int(i)]["setting"] == "1. Non-laboratory", (m["condition"], i)
        assert m["pod_method"] in {"pod sensor", "cartridge reader", "handheld analyser",
                                   "refer", "out of scope"}
        # Truth rule: anything not backed by an EDL id or GHE row must be marked Draft.
        if not m["edl5_ids"]:
            assert m["status"].startswith(("Draft", "Out of scope")), m["condition"]


def test_every_ghe_cause_addressed():
    # Every top-10 cause in LIC/LMIC gets a menu decision, even if that decision is "out of scope".
    covered = {c for m in MENU for c in m["ghe2021_cause"].split(";") if c}
    assert covered == {r["cause"] for r in GHE}


def test_parser_reads_minimal_page():
    page = """<div class="indication-text"><div><span>Discipline - </span><span>X</span></div></div>
    <div class="device-title " title="Thing &amp; stuff">Thing</div>
    <a class="section-link" href="/?section[]=2">
        <span>1. Non-laboratory</span></a>
    <a class="section-link" href="/?tieredTestingService[]=1">
          <span>Community/outreach</span></a>
    <div class="header-row"><div class="label-cell">Assay format</div>
    <div class="content-cell"><div class="with-footnotes"><div>Dipstick</div></div></div>
    </div>
    <div class="header-row"><div class="label-cell">Purpose</div>
    <div class="content-cell"><div class="with-footnotes"><div>To do it.</div></div></div>
    </div>
    First added in 2018"""
    r = parse(page, 7)
    assert r["test"] == "Thing & stuff"
    assert r["setting"] == "1. Non-laboratory"
    assert r["tiered_testing_service"] == "Community/outreach"
    assert r["assay_format"] == "Dipstick"
    assert r["purpose"] == "To do it."
    assert r["specimen_types"] == ""  # missing field stays empty, never guessed
    assert r["first_added"] == "2018"

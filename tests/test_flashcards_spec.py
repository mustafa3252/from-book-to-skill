"""Regression tests for the flashcards.md layer of the generator spec.

flashcards.md is this fork's addition to the generated-skill layout: an
active-recall deck the generated skill quizzes the user from. Nothing in this
project executes SKILL.md — these tests pin the prose the converting agent is
meant to follow, so an edit that silently drops the deck (or turns it back
into a definition index) fails here instead of surfacing as skills generated
without it.
"""

import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILL_MD = REPO_ROOT / "SKILL.md"


def _spec() -> str:
    if not SKILL_MD.is_file():
        pytest.skip("SKILL.md not present (e.g. installed sdist)")
    return SKILL_MD.read_text(encoding="utf-8")


def _flashcards_section(spec: str) -> str:
    """The `### flashcards.md` generation section, up to the next heading."""
    match = re.search(r"^### flashcards\.md$(.*?)^#", spec, re.M | re.S)
    assert match, "SKILL.md no longer has a `### flashcards.md` generation step"
    return match.group(1)


def test_flashcards_is_generated_and_indexed():
    """The deck must be created AND discoverable: a generation step, a line in
    the generated SKILL.md's Supporting Files index, and a row in the closing
    report. Missing any one of these ships skills where the deck exists but is
    never loaded, or is promised but never written."""
    spec = _spec()
    _flashcards_section(spec)
    assert "[flashcards.md](flashcards.md)" in spec
    assert spec.count("flashcards.md") >= 5


def test_cards_demand_retrieval_not_recognition():
    """The deck's reason to exist: questions that force recall. If the section
    stops distinguishing itself from the glossary, it is dead weight."""
    section = _flashcards_section(_spec())
    assert "**Q:**" in section and "**A:**" in section
    assert "glossary" in section.lower(), (
        "the spec must tell the generator NOT to duplicate glossary definitions"
    )


def test_quiz_protocol_forbids_deck_dumping():
    """Quizzing one question at a time is the feature; pasting the whole deck
    is a token-expensive way to test nothing."""
    section = _flashcards_section(_spec())
    assert "one question at a time" in section.lower()
    assert "never dump the deck" in section.lower()


def test_deck_has_a_token_ceiling():
    """SKILL.md is always-loaded converter context and generated files have
    budgets; a deck without a ceiling grows until it costs more than the
    re-reading it replaces."""
    section = _flashcards_section(_spec())
    assert re.search(r"[Mm]ax 1,000 tokens", section)


def test_update_workflow_merges_the_deck():
    """Fold-in updates must extend the deck for new chapters, not orphan it."""
    spec = _spec()
    assert "**Merge flashcards.md**" in spec

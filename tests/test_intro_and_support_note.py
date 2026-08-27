"""Two quiet messages: attribution at the start, upstream credit at the end.

The credit sits at the end on purpose — the reader has just received
something that worked, and that work stands on the upstream project this
fork is built on — and only when the run succeeded.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from from_book_to_skill import utils


class TestIntro:
    def test_names_the_project_and_the_licence(self, capsys):
        utils.print_intro()

        err = capsys.readouterr().err
        assert "from-book-to-skill" in err
        assert "MIT-licensed" in err

    def test_does_not_ask_for_money(self, capsys):
        """The start of a run has delivered nothing yet."""
        utils.print_intro()

        err = capsys.readouterr().err
        assert "sponsors" not in err.lower()


class TestSupportNote:
    def test_credits_the_upstream_project(self, capsys):
        utils.print_support_note()

        out = capsys.readouterr().out
        assert "github.com/virgiliojr94/book-to-skill" in out

    def test_goes_to_stdout_with_the_rest_of_the_report(self, capsys):
        """stderr is unbuffered and stdout is not when piped — mixing the two
        puts the closing line at the top of the run."""
        utils.print_support_note()

        captured = capsys.readouterr()
        assert captured.out.strip()
        assert captured.err == ""

    def test_stays_short(self, capsys):
        """Two lines. A wall of text here reads as a donation banner."""
        utils.print_support_note()

        lines = [ln for ln in capsys.readouterr().out.splitlines() if ln.strip()]
        assert len(lines) <= 2

# Changelog

All notable changes to from-book-to-skill are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the
project follows semantic versioning.

This project is a fork of [book-to-skill](https://github.com/virgiliojr94/book-to-skill)
by virgiliojr94; it was forked at upstream v1.4.0, whose history is recorded in
[the upstream changelog](https://github.com/virgiliojr94/book-to-skill/blob/master/CHANGELOG.md).

## [1.0.0] — 2026-08-27

Initial release of the fork.

### Added

- `flashcards.md` in every generated skill: an active-recall deck with 3–6
  cards per chapter. Questions force retrieval, not recognition; answers cite
  the chapter to re-read; the deck stays under a 1,000-token ceiling.
- Quiz protocol: the generated skill answers "quiz me" (optionally scoped to a
  chapter) by asking one question at a time and revealing the answer only
  after the user's attempt — never by dumping the deck.
- Update/fold-in workflow extends the deck for newly folded-in chapters.
- Spec regression tests (`tests/test_flashcards_spec.py`) pinning the deck's
  generation step, indexing, quiz protocol, token ceiling, and merge rule.

### Changed

- Renamed everything from book-to-skill to from-book-to-skill: the skill slug
  (`/from-book-to-skill`), the Python package (`from_book_to_skill`), and the
  CLI entry point.
- Runtime attribution lines now credit the upstream project instead of
  soliciting sponsorship (sponsor the original author at
  [github.com/sponsors/virgiliojr94](https://github.com/sponsors/virgiliojr94)).

### Removed

- Upstream-identity files that don't belong in a fork: sponsor/funding
  configuration, mascot artwork, the hosted-docs site infrastructure
  (mkdocs/CNAME), the Russian README, and upstream's security incident notice.


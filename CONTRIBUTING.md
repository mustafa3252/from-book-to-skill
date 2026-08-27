# Contributing to from-book-to-skill

Thanks for helping improve from-book-to-skill. This project turns books and documents
into structured agent skills; contributions that make extraction more robust,
generation higher-signal, or the docs clearer are all welcome.

## Ground rules

- **Measure, don't assert.** A change that claims a gain should show it — a test,
  a benchmark number from `tools/discovery_tax.py`, or a before/after. PRs that add
  weight (e.g. to `SKILL.md`, which is loaded on every run) without a demonstrated
  benefit will be asked for evidence first.
- **Keep `SKILL.md` lean.** It is the always-loaded converter spec. Prefer editing
  existing steps over adding new ones; justify net additions.
- **Never ship raw book text.** Generated skills synthesize; they never reproduce
  long passages. Respect source licenses (see the README's Copyright section).

## Development

```bash
git clone https://github.com/mustafa3252/from-book-to-skill.git
cd from-book-to-skill
python3 -m venv .venv && . .venv/bin/activate
pip install pytest ruff
python3 scripts/extract.py --check     # see which optional extractors you have
```

Run the checks the CI runs before opening a PR:

```bash
ruff check .
pytest -q
python3 tools/validate_skill.py SKILL.md
```

## Pull requests

- One focused change per PR; small and reviewable.
- **Conventional Commits** for titles and commits: `feat:`, `fix:`, `docs:`,
  `chore:`, `test:`, `ci:` … (e.g. `fix(extractor): scan full text`).
- Add or update tests for any behavior change.
- Keep `CHANGELOG.md` updated: one line per user-visible change, added in the
  same PR, under an Unreleased heading.
- CI must be green (lint, test matrix py3.10–3.13, smoke, SKILL.md validation).
- Fixes to extraction, parsing, or the generator spec are usually better sent
  upstream to [book-to-skill](https://github.com/virgiliojr94/book-to-skill),
  where every user of the original benefits — this fork tracks upstream and
  carries only the flashcards/quiz layer on top.

## Releases

Maintainers cut releases with semantic versioning:

```bash
# 1. bump version in pyproject.toml
# 2. retitle the Unreleased section of CHANGELOG.md as vX.Y.Z with today's date
# 3. commit, tag, push
git commit -am "chore(release): vX.Y.Z"
git tag vX.Y.Z && git push origin master vX.Y.Z
# 4. publish a GitHub Release using the new CHANGELOG section as notes
```

## Reporting bugs / requesting features

Open an issue using the templates in `.github/ISSUE_TEMPLATE/`. For extraction
bugs, please include the format, page count, and whether `--check` shows the
relevant extractor installed.

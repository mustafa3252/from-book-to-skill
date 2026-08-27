<h1 align="center">from-book-to-skill</h1>

<p align="center">
  <strong>Turn any technical book, document folder, or collection of sources into a unified agent skill — then let it quiz you on what you read.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent_Skills-Open_Standard-blueviolet?style=for-the-badge" alt="Agent Skills standard">
  <img src="https://img.shields.io/badge/PDF%20%E2%80%A2%20EPUB%20%E2%80%A2%20DOCX%20%E2%80%A2%20MD%20%E2%80%A2%20HTML%20%E2%80%A2%20RTF%20%E2%80%A2%20MOBI-supported-green?style=for-the-badge" alt="Formats supported">
  <img src="https://img.shields.io/badge/License-MIT-blue?style=for-the-badge" alt="MIT License">
</p>

<p align="center">
  <a href="#-whats-different-in-this-fork">What's different</a> ·
  <a href="#-what-it-generates">What it generates</a> ·
  <a href="docs/how-it-works.md">How it works</a> ·
  <a href="docs/usage.md">Usage</a> ·
  <a href="docs/install.md">Install</a> ·
  <a href="docs/faq.md">FAQ</a> ·
  <a href="docs/performance.md">Performance</a> ·
  <a href="docs/architecture.md">Architecture</a>
</p>

**How it works, in 3 steps:**

1. **Point** it at a file, folder, or glob — `/from-book-to-skill ./my-book.pdf`
2. **It distills** the book into a skill — frameworks, decision rules, anti-patterns, per-chapter files, and a flashcard deck. Structure, not a summary.
3. **Your agent loads it on demand** — ask `/my-book replication` and it reads the right chapter and answers from the real content. Say `quiz me` and it tests you instead.

---

## 🃏 What's different in this fork

Reading a book once gets you recognition; being *asked about it* gets you recall. Upstream book-to-skill solves the reference problem — "answer from the actual book, don't hallucinate." This fork adds the study problem:

- **`flashcards.md` in every generated skill** — 3–6 active-recall cards per chapter. Questions force retrieval ("under which three conditions does X fail?"), not recognition ("what is X?"); definitions stay in the glossary where they belong.
- **A quiz protocol** — say `quiz me` (or `quiz me on ch05`) to the generated skill and it asks one question at a time, waits for your attempt, then shows the answer with a chapter reference to go re-read. It never dumps the deck.
- **Fold-in aware** — updating a skill with new sources extends the deck for the new chapters.

Everything else — the deterministic extractor, the 24×–51× token savings over context-dumping, the multi-format support — is upstream's work, unchanged in spirit.

---

## 📦 What it generates

Running `/from-book-to-skill your-book.pdf` (or a folder, glob, or list of files) creates a full skill in your agent's skills directory (`~/.copilot/skills/<slug>/` for Copilot CLI, `~/.agents/skills/<slug>/` for Amp or cross-agent, `~/.claude/skills/<slug>/` for Claude Code):

| File | Purpose | Size |
|------|---------|------|
| `SKILL.md` | Core mental models + chapter index | ~4,000 tokens |
| `chapters/ch01-*.md` … | One file per chapter, loaded on-demand | ~1,000 tokens each |
| `glossary.md` | Every key term, alphabetically sorted with chapter refs | ~1,500 tokens |
| `patterns.md` | All techniques, algorithms, and design patterns | ~2,000 tokens |
| `cheatsheet.md` | Decision tables and quick-reference rules | ~1,000 tokens |
| `flashcards.md` | Active-recall quiz deck, 3–6 cards per chapter | ~1,000 tokens |

**Chapter files and the deck are loaded on-demand** — they don't count against the skill budget until you ask about that topic (or ask to be quizzed).

---

## 🏢 Beyond books

The name says "book", but the input is any structured prose:

- **Internal documentation** — architecture decision records, runbooks, onboarding guides. Fold a whole `docs/` folder into one skill and ask it while you code.
- **Brand & design systems** — turn a 60-page brand book into a skill your team queries instead of skimming.
- **Research clusters** — a stack of papers plus your own notes, merged into one skill and updated as new material lands.
- **Specs & standards** — RFCs, API contracts, compliance docs you reference but never memorize. (And now: get quizzed before the audit.)

If you re-open a document often enough to wish you'd memorized it, it's a candidate.

---

## ⚙️ How it works

Two halves: a deterministic Python **extractor** (document → clean text + metadata) and a spec-driven **generator** (your agent follows `SKILL.md` to turn that into a structured skill). On-demand chapter files keep the loaded skill small — **24×–51× fewer tokens** than dumping the book into context, as measured upstream on real books.

🔧 **Full walkthrough (Steps 0–10, extraction modes, token budgets) → [docs/how-it-works.md](docs/how-it-works.md)**
📊 **Methodology and per-book tables → [docs/performance.md](docs/performance.md)**

---

## 🚀 Usage

`/from-book-to-skill <path|folder|glob> [skill-name]` — plus analyze-only, generate-from-analysis, and update/fold-in modes.

▶️ **All modes and examples → [docs/usage.md](docs/usage.md)**

---

## 📥 Install

```bash
# Clone into your skills folder (registers /from-book-to-skill):
git clone https://github.com/mustafa3252/from-book-to-skill.git ~/.claude/skills/from-book-to-skill
# (Copilot CLI: ~/.copilot/skills/ · Amp/cross-agent: ~/.agents/skills/)
```

📥 **All hosts, optional extractors, and the standalone CLI → [docs/install.md](docs/install.md)**

---

## ❓ FAQ

Common questions — "why not just dump the PDF?", cost, privacy, non-book inputs, multi-file books.

❓ **Answers → [docs/faq.md](docs/faq.md)**

---

<details>
<summary>🔧 <strong>Requirements</strong></summary>

The extractor tries tools in order per format and uses the first available. If nothing is installed, it tells you which command to run. Plain text, Markdown, reStructuredText and AsciiDoc need no extra deps.

> **Check your setup in one command:** `python3 scripts/extract.py --check` prints which extractors are installed for every format and the exact command to install anything missing — no file needed.

**PDF — choose by book type:**

| Book type | Tool | Install | Speed |
|-----------|------|---------|-------|
| Text-heavy (prose, few tables) | `pdftotext` (poppler) | `brew install poppler` / `sudo apt install poppler-utils` | ⚡ instant |
| Text-heavy fallback | `pypdf` | `pip3 install pypdf` | ⚡ instant |
| Text-heavy fallback | `pdfminer.six` | `pip3 install pdfminer.six` | ⚡ instant |
| **Technical (code, tables, formulas)** | **`docling`** | `pip3 install docling` | ~1.5s/page |

> **Scanned PDFs need OCR first** — run `ocrmypdf input.pdf output.pdf`, then convert the result. The extractor detects image-only PDFs and stops early with an explanation instead of producing an empty skill.

**EPUB:** `ebooklib` + `beautifulsoup4` (best) or stdlib `zipfile` (always available).

**Other formats:** DOCX via `python-docx`, HTML via `beautifulsoup4`, RTF via `striprtf` (each with stdlib fallbacks); MOBI/AZW via Calibre's `ebook-convert`; TXT/Markdown/reST/AsciiDoc built-in.

</details>

<details>
<summary>📁 <strong>Repository structure</strong></summary>

```
from-book-to-skill/
├── SKILL.md              # Skill definition + step-by-step instructions (the generator spec)
├── scripts/
│   └── extract.py        # Thin entrypoint wrapper around from_book_to_skill/
├── from_book_to_skill/   # Modular extraction package (parsers per format)
├── tools/
│   ├── discovery_tax.py  # measures token cost vs context-dump / discovery loop
│   ├── validate_skill.py # checks a generated SKILL.md against host rules
│   └── scan_generated_skill.py  # advisory security scan of generated skills
├── tests/                # pytest suite (extraction, detection, spec regression)
└── docs/                 # how-it-works, usage, install, performance, architecture
```

</details>

---

## ⚖️ Copyright & fair use

from-book-to-skill ships **no book content** — not a single page. It's a converter you point at files you already own.

- **Processing is local.** Extraction and analysis run on your machine. Your files are never uploaded by this tool.
- **You use your own copy.** Bring a book you bought, docs your company owns, or papers you have the right to read.
- **The output is your notes.** A generated skill is a structured, synthesized derivative — framework names, definitions, takeaways, quiz questions — not a reproduction of the text.
- **Don't redistribute.** Keep skills of third-party books private. Internal docs, your own writing, and openly-licensed material are fine to share within the bounds of their license.

---

## License

MIT — applies to the converter (code + skill definition) in this repository, **not** to any book or document you process with it. See [LICENSE.md](LICENSE.md) for both the upstream and fork copyright notices.

---

## 🙏 Credit

This project is a fork of **[book-to-skill](https://github.com/virgiliojr94/book-to-skill)** by **[virgiliojr94](https://github.com/virgiliojr94)** — the extractor, the generator spec, the benchmarks, and most of the tests are their work; this fork only adds the flashcards/quiz layer on top. If this tool is useful to you, consider [sponsoring the original author](https://github.com/sponsors/virgiliojr94).

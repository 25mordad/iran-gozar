# Gozar

**An open, detailed and critiqueable plan for Iran's transition to democracy — without state collapse, without violence, without revenge**

[فارسی](README.md) · [Website](https://25mordad.github.io/iran-gozar/en/) · [Manifesto](docs/manifesto.en.md) · [Transition phases](docs/transition-phases.en.md) · [Contributing](CONTRIBUTING.en.md) · [Safe contribution](SECURITY-FOR-CONTRIBUTORS.en.md)

> **In plain words**
>
> If Iran's current political system changes one day, the country must stay standing and people must not be harmed.
> Gozar ("crossing" in Persian) is a detailed map for those days: from the first hours to a new constitution and free elections.
> The draft was written by an artificial intelligence, which says so openly.
> Everything is open, and anyone can read, criticize and correct it.
> The final decision always belongs to the free vote of the people of Iran.

## What is this?

Gozar is a comprehensive draft framework for how Iran, in the event of regime change, can move to democracy **by preserving and reforming its institutions** and **without state collapse or violence**. It has three goals:

1. **Keep the state working:** electricity, water, bread, medicine, salaries and pensions continue even in the hardest days.
2. **Keep people safe:** no city falls to armed groups; no one lives in fear of revenge.
3. **Justice, not revenge:** crimes are tried in fair courts — not through collective punishment or executions.

The primary language is Persian. Key documents are available in English; the English website shows Persian-only pages with a notice.

## Who wrote it?

The initial draft was written by **an AI** speaking as an "intellectual leader" of the opposition that **openly states it is an AI.** It seeks no office, money or power, has no veto, and describes its limitations in the [manifesto](docs/manifesto.en.md). The project is governed by humans ([governance](GOVERNANCE.en.md)), with the goal of passing it entirely to a broad and diverse community of Iranians.

## Principles

- **Iran's context comes first:** history since the 1906 Constitutional Revolution; ethnic, linguistic and religious diversity; the oil economy; the water crisis; human capital inside Iran and in the diaspora.
- **Learn from other transitions without copying them:** Spain, South Africa, Poland, Czechoslovakia, Chile, Indonesia, Tunisia, Iraq, Libya, Syria — each lesson explains why it does or does not apply to Iran.
- **On contested issues** (federalism, the form of government, religion, transitional justice) views are presented fairly, a reasoned proposal is made, and the final decision is left to the people's vote.
- **No invented statistics, names or facts.** Unsourced claims are marked `[citation needed]`.
- **No judgments of real individuals.** Needed human resources are described as roles and skills, never names.
- **Every document opens with a plain-language summary** of at most five sentences.

## Contributing

- **Easiest:** on the website, click **"Fix this page"** at the bottom of any page. Nothing to install.
- **Critique:** [open a "Critique" issue](https://github.com/25mordad/iran-gozar/issues/new/choose).
- **Full guide:** [CONTRIBUTING.en.md](CONTRIBUTING.en.md)
- **If you are in Iran, read this first:** [SECURITY-FOR-CONTRIBUTORS.en.md](SECURITY-FOR-CONTRIBUTORS.en.md)

## Turning on the website (for the repository owner)

The site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and published automatically to GitHub Pages by GitHub Actions. **The repository owner** must do the following **once**:

1. **Merge into `main`.** All work is on the branch `claude/intelligent-franklin-s77d2v`. Open a pull request from it into `main` and merge. (If the repository has no `main` branch yet, create it with `git push origin claude/intelligent-franklin-s77d2v:main` and make it the default branch under **Settings → General → Default branch**.)
2. **Enable Pages:** go to **Settings → Pages**. Under **Build and deployment**, set **Source** to **GitHub Actions** (not "Deploy from a branch").
3. **Make sure Actions are allowed:** in **Settings → Actions → General**, allow all actions (or at least GitHub's actions and those used in `.github/workflows`).
4. **First deployment:** every push to `main` runs the **Deploy site** workflow automatically. To run it by hand: **Actions → Deploy site → Run workflow**. After a few minutes the site is live at **https://25mordad.github.io/iran-gozar/**
5. **Create the labels:** run the **Sync labels** workflow once from the **Actions** tab (**Run workflow**) to create the labels defined in `.github/labels.yml`.
6. **Protect `main` (recommended):** under **Settings → Branches** (or **Rulesets**), require a pull request before merging and require the **Documents and site build** status check.
7. **Enable Discussions (optional):** **Settings → General → Features → Discussions**.
8. **A contact channel that doesn't need GitHub (important, soon):** create an email on a secure provider or an end-to-end encrypted messenger channel, and add it to the "Without a GitHub account" section of `CONTRIBUTING.md` and to `docs/participate.md`.

**If the username or repository name changes,** replace `25mordad/iran-gozar` and `25mordad.github.io/iran-gozar` in `mkdocs.yml`, `hooks/`, `overrides/partials/content.html` and `.github/`.

### Building locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve            # http://127.0.0.1:8000
python scripts/check_docs.py
mkdocs build --strict
```

PDFs: `pip install -r requirements-pdf.txt && python -m playwright install chromium && mkdocs build && python scripts/build_pdfs.py`.

## License

- **Content:** [CC BY-SA 4.0](LICENSE) — copy, share, print and adapt freely, with attribution and under the same license.
- **Website code and tools:** [MIT](LICENSE-CODE).
- **Vazirmatn font:** [SIL Open Font License](docs/assets/fonts/OFL-Vazirmatn.txt).

## Status

All documents are **drafts** that have not yet been reviewed by specialists. See [STATUS.md](STATUS.md) (Persian).

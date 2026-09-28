# Contributing Guide

[نسخه‌ی فارسی](CONTRIBUTING.md)

> **In plain words**
>
> Anyone can make this plan better: fix a typo, add a source, criticize a section or propose a new document.
> The simplest way is to click the pencil button on GitHub, fix the text and press the green button; you don't need to install anything.
> Volunteers called "maintainers" review your proposal and may ask questions or request changes.
> If you don't have, or don't want, a GitHub account, there are other ways too.
> If you live in Iran, first read the [safe contribution guide](SECURITY-FOR-CONTRIBUTORS.en.md).

## Contents

1. [Before you start](#before-you-start)
2. [Kinds of contribution](#kinds-of-contribution)
3. [The simple way: edit in your browser, install nothing](#the-simple-way)
4. [The professional way: fork, clone, branch and PR](#the-professional-way)
5. [Naming branches and writing commit messages](#naming-branches-and-writing-commit-messages)
6. [What to write in a PR description](#what-to-write-in-a-pr-description)
7. [Checklist before submitting](#checklist-before-submitting)
8. [Style guide](#style-guide)
9. [What happens after you submit](#what-happens-after-you-submit)
10. [Content disagreements](#content-disagreements)
11. [A good PR and a bad PR](#a-good-pr-and-a-bad-pr)
12. [Without a GitHub account](#without-a-github-account)

## Before you start

- **Safety:** if you live in Iran or have family there, read the [guide to safe, pseudonymous contribution](SECURITY-FOR-CONTRIBUTORS.en.md) first. Contributing under a pseudonym is fully accepted.
- **Principles:** read the [project manifesto](docs/manifesto.en.md). Every contribution must be consistent with its values and red lines.
- **Conduct:** accept the [Code of Conduct](CODE_OF_CONDUCT.en.md). Attack ideas, not people.
- **Vocabulary:**

| Term | Meaning |
|---|---|
| **Repository** | This project on GitHub: all its files and their history |
| **Issue** | A public note to report a problem, criticize or suggest something, without changing the text |
| **PR** (pull request) | A proposal for a specific change to the text, which others review and, if approved, merge into the main text |
| **Fork** | Your personal copy of the whole repository, where you can change things freely |
| **Branch** | A separate line of work that holds your changes until they are ready |
| **Commit** | A recorded change with a short description |
| **Maintainer** | A volunteer who reviews and merges PRs. See [Governance](GOVERNANCE.en.md) |

## Kinds of contribution

| Kind | Example | Best route | Difficulty |
|---|---|---|---|
| **Fix a typo** | a missing half-space in Persian | Direct edit (simple way) | Very easy |
| **Add a source** | Replace a "[citation needed]" with a reliable source | Direct edit | Easy |
| **Correct content** | Fix a wrong fact or a weak argument | Direct edit or professional way | Medium |
| **Critique a section** | "This proposal won't work in border provinces, because…" | Issue of type "Critique" | Easy |
| **Propose a new document or institution** | "We need a document on agriculture and food security" | Issue first, then PR | Hard |
| **Translate** | Translate a document into English or another language of Iran | Professional way or direct edit | Medium |
| **Help with the website** | Improve mobile layout, fix search | Professional way | Medium–hard |
| **Review** | Read others' PRs and comment | The Pull requests tab | Easy |

**Tip:** "[citation needed]" markers are the best place to start. On the website, the [Sources needed](docs/needs-sources.md) page lists all of them. Issues labeled `مبتدی-پسند` (good first issue) are also good starting points.

## The simple way

Editing in your browser, with nothing to install, is enough for most contributions. You only need a GitHub account.

**Step 0 — Create a GitHub account.** Go to github.com and click **Sign up**. If you are in Iran, read the [safe contribution guide](SECURITY-FOR-CONTRIBUTORS.en.md) first so that the account is not linked to your real identity.

**Step 1 — Find the file.** Either:

- **From the project website:** at the bottom of every page there is a **"Fix this page"** button that takes you directly to the editor for that file on GitHub (then skip to step 3); or
- **From GitHub:** open the `docs` folder. Institution documents are in `docs/institutions`, topics in `docs/topics`. English versions end in `.en.md`.

**Step 2 — Click the pencil.** Above the file content there is a **pencil ✏️ icon** titled **Edit this file**. Because you are not allowed to change the main repository directly, GitHub **automatically creates a personal copy (fork)** and opens the file there for editing. Nothing in the main text changes until maintainers approve. If you see "You need to fork this repository to propose changes", click **Fork this repository**.

**Step 3 — Edit the text.** Files use **Markdown**; most of it is plain text. Lines starting with `#` are headings; `**text**` is bold; `[link text](address)` is a link; lines starting with `>` (such as the "In plain words" box) form a separate box. Only change the "front matter" between the two `---` lines if you know what you are doing. The **Preview** tab shows the rendered result.

**Step 4 — Commit changes.** Click the green **Commit changes…** button. In the dialog:

- **Commit message:** one short sentence about what you did, e.g. `police: fix typo`. See [commit messages](#naming-branches-and-writing-commit-messages).
- **Extended description:** optional; explain why, especially if you added a source.
- The option **Create a new branch for this commit and start a pull request** is usually preselected: your change is saved in a new branch and a pull request is started right away.
- Click **Propose changes**.

**Step 5 — Open the pull request.** On the **Open a pull request** page:

- The top shows where the change goes (from your branch in your fork to `main` in the main repository). No need to change anything.
- **Title:** a clear sentence, usually your commit message.
- **Description:** a prepared template with a checklist appears. Fill it in: what changed, why, where the source is.
- Review your changes at the bottom (green = added, red = removed).
- Click **Create pull request**.

**Done!** Automated checks run (e.g. links are valid and the site builds without errors), and a maintainer will review it. To add more changes to the same PR, open its **Files changed** tab, click **⋯** next to the file name, then **Edit file**.

## The professional way

Fork, clone, branch, commit, push and PR. This suits larger changes, work on several files, or work on the website. You need `git`, and `python` to preview the site locally.

> **If you are in Iran:** before your first commit, complete the "git and commits" section of the [safe contribution guide](SECURITY-FOR-CONTRIBUTORS.en.md). Every commit records your name, email and time zone.

```bash
# 1. Fork on GitHub (button at the top of the repository page), then clone:
git clone https://github.com/<your-username>/iran-gozar.git
cd iran-gozar
git remote add upstream https://github.com/25mordad/iran-gozar.git

# 2. Branch from the latest main
git checkout main
git pull upstream main
git checkout -b source/central-bank-inflation

# 3. Preview the site locally
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
mkdocs serve                       # open http://127.0.0.1:8000

# 4. Run the checks
python scripts/check_docs.py
mkdocs build --strict

# 5. Commit
git add docs/institutions/central-bank.md
git commit -m "central-bank: add source for inflation rate" -m "Source: CBI annual report, table 2"

# 6. Push
git push -u origin source/central-bank-inflation
```

**7. Pull request:** open your fork on GitHub, click **Compare & pull request**, fill in the template and click **Create pull request**.

**8. Staying up to date** while your PR is open:

```bash
git checkout main && git pull upstream main
git checkout source/central-bank-inflation && git merge main && git push
```

## Naming branches and writing commit messages

**Branch names:** `type/short-description-in-english` (lowercase Latin letters, words separated by hyphens).

| Type | For | Example |
|---|---|---|
| `fix` | Typos, formatting, broken links | `fix/typo-police` |
| `source` | Adding or correcting sources | `source/water-subsidence-data` |
| `content` | Substantive change to a document | `content/judiciary-vetting` |
| `new` | New document or institution | `new/agriculture-food-security` |
| `translation` | Translation | `translation/faq-en` |
| `site` | Website, design, tooling | `site/share-button` |
| `project` | The project's own rules and documents | `project/governance-quorum` |

**Commit messages:**

```text
<area>: <one-line summary, about 70 characters max>

<optional body: why was this needed? where is the source?>
```

`area` is the file or section name (`police`, `manifesto`, `site`, `faq`…). Start the summary with a verb: "add…", "fix…", "remove…". Persian or English are both fine.

Good: `police: add UN principles on the use of force` · Bad: `update`, `changes`, `fixed stuff and added more things to several files`.

## What to write in a PR description

The PR template loads automatically. Answer three questions:

1. **What changed?** One or two sentences.
2. **Why?** e.g. "The previous number had no source and did not match the official report."
3. **Where is the source?** Name, publisher, year and, if possible, a link — plus an archived link (e.g. web.archive.org), because links disappear or get filtered.

If your change relates to an issue, write `Closes #<issue-number>`.

## Checklist before submitting

- [ ] **Sourced?** Every new factual claim (number, event, law) has a source or is marked "[citation needed]".
- [ ] **Plain summary updated?** If the document's main message changed, the "In plain words" summary at the top is updated and still has at most 5 sentences.
- [ ] **Consistent with the project's principles?** It does not contradict the [manifesto](docs/manifesto.en.md), values or red lines.
- [ ] **Respectful tone?** No insults, labels or judgments about real individuals.
- [ ] **Safe?** Contains no identifying information about you or others.
- [ ] **Fair?** On contested issues, opposing views have not been removed or distorted.
- [ ] **One topic only?** The PR contains one coherent change, not several unrelated ones.

## Style guide

**Tone:** calm, precise and respectful. Our readers are both specialists and ordinary citizens — both opponents of the current system and people who work within it. Write about structures and behaviors, not individuals. Be humble about what we don't know, and clear about what we propose and why.

**Preferred terms:**

| Instead of | Write | Why |
|---|---|---|
| "regime" (as an insult) | the current system, the Islamic Republic | Descriptive, not demeaning |
| purge, cleansing | individual vetting | Responsibility is individual, not collective |
| revenge, settling scores | accountability, fair trial | The goal is justice |
| mercenary, traitor, infiltrator | (describe the specific behavior) | Labels replace arguments |
| after the fall | after day zero, during the transition | Scenarios differ |
| ethnic minorities | ethnic and linguistic communities | Some prefer "nations/nationalities"; use terms respectfully and avoid demeaning ones |
| "exiles" (dismissive) | Iranians abroad, the diaspora | Neutral and respectful |

**Persian orthography** (for Persian texts): use the zero-width non-joiner (half-space) correctly; Persian ی and ک, not Arabic ي and ك; Persian digits in Persian text; Persian quotation marks «»; Iranian events dated in the Solar Hijri calendar with the Gregorian year in parentheses.

**Sources and citations:**

- Every specific factual claim needs a **source**.
- If you have none, don't delete the claim: mark it `[citation needed]` in English texts or `[نیاز به منبع]` in Persian texts.
- **Never invent a source.** A fake source is worse than none.
- List sources in a "## Sources" section at the end: books as `- Author, *Title*, Publisher, Year.`; reports as `- Organization, "Title", Year. [link](address)`; laws as `- Constitution of the Islamic Republic of Iran, Article 110.`
- Prefer **primary sources**, and give archived copies of web links when possible.
- **Real individuals:** never accuse or judge a person by name. Define needed human resources as **roles and skills**, not names.

**Document format** (full templates in [templates](templates/)): front matter (`title`, `description`, `status`) between `---` lines; an `#` title; the plain-language summary (max 5 short sentences, no jargon) as a blockquote starting with `> **In plain words**` (English) or `> **خلاصه به زبان ساده**` (Persian); `##` sections and `###` sub-sections; "Open questions for public discussion"; "Sources". Status values: `draft`, `review`, `reviewed`.

## What happens after you submit

1. **Automated checks** run within minutes: link validity, site build, document format (e.g. the plain summary exists). If one fails, click **Details**; if unclear, ask in the PR.
2. **Labeling:** a maintainer adds labels (e.g. `محتوا` content, `ترجمه` translation) and assigns a reviewer.
3. **Review:** the reviewer approves, requests changes (explaining what), or comments.
4. **Public comment period:** content changes stay open at least 7 days, changes to principles at least 30 days. See [Governance](GOVERNANCE.en.md).
5. **Merge or rejection.**

Labels are defined in [`.github/labels.yml`](.github/labels.yml); names are in Persian with English descriptions.

**How long will it take?** We aim to respond **within 7 days**. Everyone is a volunteer; if you hear nothing after 14 days, leave a polite reminder in the PR.

**If changes are requested:** that is normal and good — someone read your text seriously. Apply the changes in the same branch (the same PR updates; don't open a new one), or explain respectfully why you disagree. Reviewers can be wrong too.

**If your PR is rejected:** the maintainer must give a reason referring to the [acceptance criteria](GOVERNANCE.en.md#acceptance-criteria). You may request one review by another maintainer. A rejected PR means the text was not accepted in that form — not that you or your view are worthless. Improve it and resubmit, or open a "Critique" issue to continue the discussion.

## Content disagreements

Disagreement about content is **welcome**; this plan only improves through criticism.

- **Issue first, then PR.** If you disagree with a fundamental proposal (e.g. on federalism or the form of government), open a "Critique" issue with your argument instead of rewriting directly.
- **Arguments and sources, not pressure.** The number of supporters doesn't decide; the quality of the argument does.
- **Value disagreements are not solved by deletion.** Usually the solution is to include your view, with its strongest argument, in the document's "Different viewpoints" section.
- **Formal process:** discussion → mediation → maintainers' council vote → recorded in [decisions.md](docs/decisions.md). Details in [Governance](GOVERNANCE.en.md#dispute-resolution).

## A good PR and a bad PR

**Good:**

> **Title:** `water-environment: add source for land subsidence in major plains`
>
> **What changed:** In "Current situation", I completed the subsidence sentence that was marked "[citation needed]" with a source and added the names of two plains mentioned in the report.
>
> **Why:** This claim is one of the document's key arguments; without a source, critics could dismiss it.
>
> **Source:** publishing organization, report title, year, page number, original and archived links.

*Why it is good:* one specific change; a clear title; precise reason and source; a reviewer can check it in minutes.

**Bad:**

> **Title:** `changes`
>
> **Description:** This document was very weak and the author obviously knows nothing about Iran. I completely rewrote the IRGC section because everyone knows it must be dissolved. I also fixed a few other places.

*Why it is bad:* the title says nothing; the tone attacks the author instead of the argument; a major contested change is made without a prior issue, argument or source ("everyone knows" is not a source); other viewpoints are deleted; several unrelated changes make review nearly impossible. *How it could have been good:* a "Critique" issue arguing why full dissolution is better and which countries' experience supports it, plus separate PRs for the small fixes.

## Without a GitHub account

If you don't have a GitHub account, don't want one, or creating one is dangerous for you:

1. **Through a trusted intermediary.** Give your comment to someone you trust (preferably outside Iran) to open an issue in their own name. For many people in Iran this is the safest route.
2. **Direct project contact channels.** Maintainers should set up at least one channel that does not require GitHub (e.g. an email on a secure provider, or an end-to-end encrypted messenger). **These channels are not set up yet**; once they are, their addresses will appear here and on the website's [How can I take part?](docs/participate.md) page. Anything received through them is posted in a public issue **without any identifying information**, with only the text of the comment, unless you ask otherwise.
3. **In-person discussion.** Read the documents (e.g. the PDF versions) with people you trust and collect their critiques. Even if they never reach us, that conversation is itself part of preparing for a transition.

**Warning:** no maintainer will ever ask you for your real name, phone number, address, password or money. Anyone asking for these in the project's name is a fraud.

---

Thank you for your time. Every small correction makes this map a little more accurate for the day it is needed.

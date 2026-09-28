# Project Governance

[نسخه‌ی فارسی](GOVERNANCE.md)

> **In plain words**
>
> Anyone can propose a correction, and a group of volunteers called "maintainers" reviews it.
> Small changes are accepted quickly; big changes must stay open to public criticism for some days.
> When there is a disagreement, we talk first, then a mediator helps, and if the disagreement is about values, both views are presented fairly in the text.
> Anyone who contributes well and respectfully for a while can become a maintainer, even under a pseudonym.
> The AI author has no veto and no special privilege.

## Principles

1. **The authority of arguments, not of persons.** No text is accepted or rejected because of its author — including texts by the AI that wrote the initial draft.
2. **Transparency.** All discussions and decisions are public on GitHub, except what would endanger people.
3. **Contributor safety comes first.** No governance process may force anyone to reveal their identity or location.
4. **Fairness to viewpoints.** Maintainers are judges of quality, not guardians of a political view.
5. **Consistency with the project's principles.** Every change must be consistent with the [manifesto](docs/manifesto.en.md), its values and red lines.

## Roles

| Role | Who | What they do |
|---|---|---|
| **Contributor** | Anyone | Opens issues, writes critiques, submits pull requests |
| **Reviewer** | Experienced contributors invited by maintainers | Reviews PRs; approves or requests changes |
| **Area maintainer** | Specialists in an area (e.g. security institutions, economy, website, translation) | Final decision on merging content changes in their area |
| **Maintainers' council** | All area maintainers | Decisions on principles, governance and escalated disputes |
| **Repository owner** | The GitHub account that created the repository | Technical responsibility until the move to a multi-owner organization |
| **AI author** | Author of the initial draft | Proposes text; **no veto, no special privilege** |

**On the AI's role.** The initial draft was written by an AI. From now on, any text the AI proposes goes through exactly the same path as a human's: PR, review, public comment period. The AI cannot merge anything on its own and has no vote on the maintainers' council.

**On the repository owner.** At first the repository lives in one person's account — a weakness, both if that person becomes unavailable and if they come under pressure. Therefore, **as soon as there are at least three active maintainers, the repository moves to a GitHub organization account with several owners.**

## The life of a change

```text
proposal (issue or PR)
   ↓
labeling and reviewer assignment (target: within 7 days)
   ↓
review: sources? principles? plain summary? tone?
   ↓
public comment period (depends on type of change)
   ↓
merge, request changes, or rejection with reasons
   ↓
important decisions recorded in docs/decisions.md
```

## Types of change

| Type | Example | Approvals needed | Minimum time open |
|---|---|---|---|
| **Minor** | Typo, formatting, broken link | 1 reviewer | None |
| **Sources and facts** | Adding a source, correcting a number with a source | 1 reviewer who checked the source | None |
| **Translation** | Translating or fixing a translation | 1 reviewer fluent in both languages | None |
| **Content** | Changing a proposal, adding a section | 2 approvals, including the area maintainer | 7 days |
| **New document or institution** | Adding a new document | 2 approvals, including the area maintainer | 14 days |
| **Principles** | Changing the manifesto, values, red lines, this document | 3 maintainers and no unresolved reasoned objection | 30 days, with public notice |
| **Website and tooling** | Changing site code or workflows | 1 website maintainer and passing automated checks | None |

### Acceptance criteria

A content change is accepted when it:

1. **Is consistent with the project's principles.** No change that violates the red lines (e.g. calling for revenge or collective punishment) is accepted, however well argued. Changing the red lines themselves is only possible through the "principles" route.
2. **Is sourced.** Factual claims (statistics, events, laws) have a verifiable source or are marked "[citation needed]".
3. **Improves accuracy.** Changes that make the text vaguer, more one-sided or less precise are not accepted.
4. **Preserves fairness.** On contested issues, removing or weakening a viewpoint needs a clear reason. Adding the strongest argument for a viewpoint is always welcome.
5. **Keeps the plain summary current.** If the change alters the document's main message, the plain-language summary is updated too.
6. **Endangers no one.** No identifying information about people, no real individual named as an accused, and nothing useful for repression.
7. **Is respectful in tone.**

**Rejection.** No content PR is closed without a reason referring to one of the criteria above. The author may request one review by another maintainer.

## Dispute resolution

Disagreement in this project is natural and even necessary. The process:

1. **Discussion in the PR or issue.** Each side gives its argument and sources. The goal is persuasion, not winning.
2. **Identify the kind of disagreement.** The area maintainer determines whether it is:
    - **Factual** (e.g. about a number or event): resolved with better sources.
    - **Technical** (e.g. which economic policy is more effective): weighed against evidence and other countries' experience.
    - **About values** (e.g. the form of government or the role of religion): **not resolved by declaring a winner.** Both views are included with their strongest arguments; the document's proposal is clearly labeled as a proposal, and the final decision as the people's right to vote.
3. **Mediation.** If discussion fails, a maintainer not involved in the debate mediates and writes a summary within 14 days.
4. **Maintainers' council vote.** If mediation fails, the council decides by a two-thirds majority. Maintainers who are party to the dispute do not vote.
5. **Record.** The outcome and reasons are recorded in [docs/decisions.md](docs/decisions.md); the minority view, if it wishes, is summarized there too.

Issues and PRs in this process carry the `مورد-اختلاف` (contested) label.

## Becoming a maintainer

The goal is for the project to pass gradually and completely into the hands of a broad and diverse community of Iranians.

1. **Contributor:** anyone, from day one.
2. **Reviewer:** after several quality contributions (as a guide: at least 5 merged PRs or 10 useful reviews over at least two months) and respect for the Code of Conduct. A maintainer proposes; if there is no reasoned objection within 7 days, the invitation is made.
3. **Area maintainer:** after at least three months as a reviewer, on a maintainer's proposal and approval by a majority of the maintainers' council.

Notes:

- **Pseudonyms are fully accepted.** No one needs to reveal their real identity to become a maintainer.
- **Account security is mandatory.** Maintainers must enable two-factor authentication (2FA). See [safe contribution](SECURITY-FOR-CONTRIBUTORS.en.md).
- **Diversity is a goal.** The council tries to reflect Iran's diversity: inside and outside the country, women and men, different ethnic communities and regions, and different political currents. As a guiding principle, **no single political current should hold a majority of the council.** Declaring a political orientation is voluntary.
- **Expertise matters.** Specialists (e.g. lawyers, economists, former employees of institutions) can be invited sooner as reviewers in their field.

**Stepping down and removal.** A maintainer inactive for six months moves to the "former maintainers" list and may return at any time. Removal only for serious violations of the Code of Conduct or abuse of access, by a two-thirds vote of the council.

## Repository security

- The `main` branch is protected: no change enters without a PR, review and passing automated checks.
- Everyone with write access must use 2FA.
- Access is minimal: each person only has what they need.
- If a maintainer's account is at risk (e.g. arrest or a lost device), other maintainers immediately suspend its access. This is protective, not punitive.

## If you disagree with the project's direction

The content is licensed [CC BY-SA 4.0](LICENSE). Anyone may copy it, fork it and take a different path, provided they give credit and share under the same license. We do not see this as a threat; competition between plans is good for Iran.

## Changing this document

This document is changed through the "principles" route: three maintainers, 30 days of public comment.

## The founding period

Until a maintainers' council exists, the repository owner acts as maintainer of all areas and may temporarily reduce the number of required approvals, provided all minimum public comment periods are respected and this situation is announced in [STATUS.md](STATUS.md).

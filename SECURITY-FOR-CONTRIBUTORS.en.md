# Safe and Pseudonymous Contribution

[نسخه‌ی فارسی](SECURITY-FOR-CONTRIBUTORS.md)

> **In plain words**
>
> If you live in Iran, contributing to this project may be dangerous for you, and no method gives complete safety.
> If you decide to contribute, build a completely separate online identity: a pseudonym, a separate email and a separate GitHub account not linked to your phone number or real accounts.
> Always connect through Tor or a reputable VPN, and never use your workplace's devices or internet.
> Remove hidden information from any photo or file before sending it, and never mention your city, job or family in your texts.
> If you are unsure, don't contribute directly, or send your comments through a trusted intermediary abroad.

This is a condensed English version of the Persian guide. The Persian version is authoritative and more detailed.

## Take the risk seriously

This guide reduces risk; it does **not** eliminate it. No tool is perfectly safe, and this guide is not a substitute for professional digital-security or legal advice. Under the current system, even peaceful political activity may carry serious legal consequences. [citation needed: documented prosecutions for online activity]

Ask yourself first: *Is anyone watching me?* (known activists, employees of sensitive institutions and former detainees face higher risk) · *What happens if my identity is exposed — to me, my family, my colleagues?* · *Is there a lower-risk way?* Reading, sharing, or commenting through an intermediary abroad carries far less risk than committing directly.

| How you could be identified | Countermeasure |
|---|---|
| Internet traffic monitoring by your provider | Tor or a reputable VPN |
| Linked accounts (shared email, phone number, username) | A fully separate identity |
| File metadata (location, device, time, author name) | Remove metadata, or don't send files |
| Git data (name, email and **time zone** in every commit) | Configure git correctly (section 5) |
| Behavior (activity hours, writing style, personal details) | Vary timing; write carefully |
| Device searches at checkpoints or on arrest | Strong lock, encryption, logging out |
| Phishing (fake login pages, fake "support" messages) | Check addresses; use 2FA |

## 1. Build a separate identity

- **Pseudonym:** new, unrelated to any name or username you have used before.
- **Email:** new, from a privacy-respecting provider abroad (e.g. Proton Mail or Tuta), created over Tor or a VPN. Never use domestic email services, work or university email, or anything tied to your Iranian SIM card.
- **GitHub account:** created with that email over Tor/VPN; no real name, photo, location or bio. Enable **two-factor authentication with an authenticator app, not SMS**, and keep the recovery codes on paper. In **Settings → Emails**, enable **Keep my email addresses private** and **Block command line pushes that expose my email**.
- **Never mix identities:** don't use the pseudonymous account in the same browser as your real accounts. Ideally, use it only in Tor Browser.

## 2. Connect safely: VPN vs Tor

A **VPN** hides your traffic from your internet provider, but the **VPN company** sees everything; free or unknown VPNs may themselves be surveillance tools. **Tor** routes traffic through several independent relays so that none knows both who you are and where you connect; it is built for **anonymity**, while most VPNs and circumvention tools are built for **access**. Use **Tor Browser** for your pseudonymous account, downloaded only from the Tor Project's official channels; where Tor is blocked, use **bridges** (Tor Browser can choose them automatically; options such as Snowflake are designed for heavy censorship). Always check you are on `github.com`, and never give a code or password to anyone who messages you — maintainers never ask for them.

## 3. Secure your device

Keep your system updated; avoid work, shared or internet-café computers; use a strong screen lock and full-disk encryption; don't stay logged into GitHub on your phone. For high-risk people: consider **Tails**, an operating system that runs from a USB stick, routes everything through Tor and leaves no trace on the computer.

## 4. Metadata

Photos can contain GPS location, device model and time; screenshots can show your carrier, clock and usernames; Word/PDF files can contain the author's name and edit history. **Simple rule: don't send files — type text.** If you must, strip metadata (e.g. `mat2 photo.jpg` on Linux/Tails, or `exiftool -all= photo.jpg`), check again, and crop screenshots.

## 5. Git and commits: name, email and time zone

Every git commit permanently records the **author name**, **author email**, and the **time with your computer's time zone offset**. Iran's offset is `+0330`: if your computer uses Iran time, **every commit says you are in Iran.**

```bash
git config --global user.name "your-pseudonym"
git config --global user.email "12345678+username@users.noreply.github.com"   # from Settings → Emails

TZ=UTC git commit -m "message"     # this commit only
export TZ=UTC                      # for this whole terminal session

git log --format='%an <%ae> %ad' -5   # check before every push: pseudonym, noreply email, +0000
```

If you made a mistake and **haven't pushed**: `TZ=UTC git commit --amend --reset-author --no-edit` (or recreate your changes on a fresh branch). If you **already pushed**, tell the maintainers immediately and privately; full removal from the internet may not be possible, so speed matters.

If you edit in the GitHub website, check your first commit anyway: add `.patch` to the end of the commit's address and inspect the `From:` and `Date:` lines.

## 6. Behavior and writing style

Vary your activity hours; don't write "in our city…", "in our office…"; don't paste texts you published elsewhere under your real name; avoid details only a few people know.

## 7. If you work in a state institution

Your knowledge of how institutions really work is valuable — and riskier. Never publish classified documents (the project doesn't need them; it needs structural understanding); generalize details; never use work devices or networks; if unsure, use an intermediary.

## 8. If something goes wrong

If your account may be compromised: close all sessions in **Settings → Sessions**, change your password and regenerate recovery codes. Agree in advance with a trusted person (ideally abroad) to alert the maintainers if you are arrested or lose your device, so your project access can be suspended immediately. You can delete your GitHub account; your contributions remain but are no longer attributed to your username.

## 9. Lower-risk ways to help

Read and share (the website has no trackers, advertising cookies or external resources, and PDFs can be shared offline); discuss the documents in person with people you trust; give your comments to a trusted intermediary abroad; see "[Without a GitHub account](CONTRIBUTING.en.md#without-a-github-account)" in the contributing guide.

## Further reading

The EFF's *Surveillance Self-Defense*; *Security in a Box* by Front Line Defenders and Tactical Tech; the Tor Project's documentation on bridges and Tor Browser; Access Now's Digital Security Helpline; GitHub's documentation "Setting your commit email address".

**If you are a digital-security specialist, your review of this guide matters more than anywhere else in the project.**

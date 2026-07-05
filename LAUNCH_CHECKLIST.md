# Launch Checklist

What you need to do (after this package is in your hands). Sequenced for ~1 day of execution.

---

## Phase 0 — Pre-launch hygiene (1 hour)

Before anything goes public, do these:

- [ ] Read the paper draft (`paper/paper.md`) end-to-end. Mark anything you don't believe or can't defend.
- [ ] Search every `VERIFY` marker in `cards/*.yaml` and check it against the current public framework document. Fix any inaccuracies. This is non-negotiable — these will be the most-scrutinized claims in the paper.
- [ ] In each card, change `notes.verification_status` from `draft` to `self_verified` once you have done a sanity read.
- [ ] Replace `Kanupriya Yakhmi`, `kanupriyayakhmi@gmail.com`, `[github-url]`, and `[github-pages-url]` placeholders in `paper/paper.md` and `README.md`.
- [ ] Decide on a paper title. Default: *Safety Framework Cards: A Standardized Specification for Documenting Frontier AI Safety Commitments.* You may want to shorten to *Safety Framework Cards for Frontier AI* for the arXiv title slot.

---

## Phase 1 — GitHub repo (30 minutes)

- [ ] Create a public GitHub repository named `safety-framework-cards` under your account or a project org.
- [ ] Push the entire `safety-framework-cards/` directory.
- [ ] In repo Settings → Pages, enable GitHub Pages from the `main` branch, `/docs` folder.
- [ ] Verify the rendered site is live at `https://<your-handle>.github.io/safety-framework-cards/`.
- [ ] Update `README.md` and `paper/paper.md` with the live URL.
- [ ] Add topics on the repo page: `ai-safety`, `ai-governance`, `frontier-ai`, `transparency`, `responsible-ai`.

---

## Phase 2 — arXiv post (1 hour)

You already have an arXiv account with endorsement — good.

- [ ] Convert `paper/paper.md` to PDF. Options:
  - Quickest: paste into Overleaf with a standard article template, or
  - Use `pandoc paper/paper.md -o paper.pdf --pdf-engine=xelatex`
  - If you want a specific workshop's LaTeX template, copy your content into it now.
- [ ] Submit to arXiv with categories: **primary `cs.CY`** (Computers and Society), **secondary `cs.AI`**.
- [ ] In the abstract submission form, paste the abstract directly from the paper (Section 0).
- [ ] In the "Comments" field, write: *"9 pages + appendices. Reference implementation, schema, and nine worked-example cards available at [github-url]."*
- [ ] Submit and wait for moderation (usually 1 business day).

---

## Phase 3 — Personal outreach (2–3 hours)

This is the lever for adoption. Send all of these on the **same day** the arXiv link goes live. Use the templates in `outreach/`.

### Pre-readers (skip if you ran a pre-read round before posting)
- [ ] Send `outreach/prereader_email.md` to 3–5 names from `outreach/contacts.csv` filtered to "pre-read" priority.

### Lab safety teams (the adoption pitch)
For each of the eight labs whose card is in the repo:

- [ ] Anthropic — send the personalized email (template: `outreach/lab_safety_team_email.md`) with their card attached as YAML and a link to the rendered HTML.
- [ ] OpenAI
- [ ] Google DeepMind
- [ ] Meta
- [ ] Amazon
- [ ] Microsoft
- [ ] xAI
- [ ] Mistral
- [ ] (Cohere, if including the ninth card)

Track responses in `outreach/contacts.csv` (Status column).

### Frontier Model Forum
- [ ] Send `outreach/fmf_pitch.md` to FMF contact (info@frontiermodelforum.org plus known program leads).

### Adjacent policy / safety community
- [ ] METR — research@metr.org
- [ ] Apollo Research
- [ ] GovAI (Centre for the Governance of AI)
- [ ] Centre for AI Safety
- [ ] IAPS (Institute for AI Policy and Strategy)
- [ ] RAND TASP
- [ ] UK AISI
- [ ] US AISI (NIST)

Many of these will see it via X/LinkedIn but a direct note doubles response rate.

### Social
- [ ] Post on X with the arXiv link, GitHub link, and a short pitch — "Spec for frontier safety frameworks, additive to existing RSPs/Preparedness Frameworks/FSFs. 9 worked cards in the repo. Comments open."
- [ ] Post on LinkedIn (longer-form, audience = policy / industry).
- [ ] Post on LessWrong with a 200-word summary.
- [ ] Post on EA Forum (same summary).
- [ ] EleutherAI Discord #governance channel.

---

## Phase 4 — Follow-through (week 2 onward)

- [ ] After 5 working days, send a single bump email to non-responders. One bump only.
- [ ] Maintain an `ADOPTION_LOG.md` in the repo: every citation, press mention, lab response, regulator interest. This file is EB1A evidence — keep it current.
- [ ] After 30 days, publish v0.2 of the spec incorporating issue/PR feedback. Tag contributors in the release notes.
- [ ] Watch NeurIPS 2026 workshop CFPs (Aug–Sept). Target SoLaR, ML Safety Workshop, governance workshops. Submit when CFP opens.
- [ ] After three months on arXiv, run a citation report (Google Scholar, Semantic Scholar). Save as PDF for EB1A documentation.
- [ ] Once any single lab adopts officially, **immediately** draft a press note and pitch tech press (TechCrunch, MIT Tech Review, FT AI desk, Wired). First adoption is the cascade trigger.

---

## EB1A documentation hygiene (continuous)

- [ ] Save every email exchange with safety teams, FMF, regulators, journalists.
- [ ] Save every public mention of the spec (tweet screenshots, blog citations, press).
- [ ] Save citation count snapshots quarterly from Google Scholar and Semantic Scholar.
- [ ] Save GitHub star history quarterly (use star-history.com or Wayback Machine).
- [ ] When you submit to workshops/conferences, save acceptance/reject letters and reviewer comments.
- [ ] When you are asked to review for any related venue, save the invitation email — it counts toward the "judging the work of others" EB1A criterion.

---

## Failure modes to watch for

- **No lab responds in week one.** Normal — most safety teams are busy. The follow-up bump is what moves them. Do not over-bump.
- **A lab corrects a factual error in their card.** This is success, not failure. Update the card with `publisher_verified` status, credit them in acknowledgments, push a v0.1.1 patch.
- **A reviewer says "this is just Model Cards for frameworks."** That's the pitch. Section 2.3 of the paper makes this explicit on purpose.
- **A lab publishes a competing spec.** Engage immediately. Offer to merge specs or be cited as prior art. Either outcome is fine for EB1A; what is bad is silent overlap.
- **You miss a NeurIPS workshop CFP.** Submit to AIES 2027 instead (deadlines May 2027). FAccT 2027 (Jan 2027) is also a fit.

---

## Final sanity check before pushing to GitHub

- [ ] Run `python validator/safety_card.py lint cards/` one more time. All nine should pass.
- [ ] Run `python renderer/render.py site cards/ -o docs/` and open `docs/index.html` in a browser. Click through.
- [ ] Spot-check the paper PDF.
- [ ] Confirm placeholders are all filled.
- [ ] Confirm LICENSE is present and reflects your name.
- [ ] Push.

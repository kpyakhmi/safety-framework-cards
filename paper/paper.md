# Safety Framework Cards: A Standardized Specification for Documenting Frontier AI Safety Commitments

**Kanupriya Yakhmi**
*PhD candidate in AI*
`kanupriyayakhmi@gmail.com`

---

## Abstract

Look at any major frontier AI lab today and you'll find a public safety framework. Anthropic published its Responsible Scaling Policy in September 2023, then revised it four times, most recently to v3.1 in April 2026. OpenAI shipped the Preparedness Framework and moved it to v2.0 in April 2025. DeepMind followed with the Frontier Safety Framework, now at v3.0 (September 2025). Meta, Amazon, Microsoft, Cohere, and xAI have their own. Every document is a wall of prose. Every one is structured differently. That's the problem.

Regulators keep asking whether these things are actually comparable to each other. Insurers ask it too. So does the Frontier Model Forum. Nobody has a good answer right now, because answering means reading every framework end-to-end.

The answer should be yes, and this paper argues that the way to get there is a shared machine-readable format. I call it a Safety Framework Card. Six structural dimensions: risk ontology, capability thresholds, evaluation methodology, mitigation commitments, governance triggers, revision protocol. The spec itself is a JSON schema. I retrofit eight published frameworks into cards, and a ninth card documents Mistral's non-publication, which is itself a finding worth reporting. An open-source validator and an HTML renderer ship alongside the paper.

Across the nine cards, the audit surfaces three convergences, four divergences, and one universal disclosure gap. Design-wise, the paper copies the Model Cards (Mitchell et al., 2019) and Datasheets for Datasets (Gebru et al., 2021) playbook. Propose a standardized artifact. Ship a reference implementation. Let adoption follow.

**Keywords:** AI safety, AI governance, frontier models, transparency, technical standards

---

## 1. Introduction

Something interesting happened between September 2023 and today. Every major frontier AI laboratory published a safety framework. Anthropic went first, with the Responsible Scaling Policy in September 2023, and has iterated it four times since (the current version is v3.1, April 2026). OpenAI hit v2.0 of the Preparedness Framework in April 2025. DeepMind reached v3.0 of the Frontier Safety Framework in September 2025. Meta, Amazon, Microsoft, Cohere, and xAI followed with their own documents. At the May 2024 Seoul AI Safety Summit, sixteen frontier developers signed onto a common set of commitments. By December 2025, twelve of them had translated those commitments into formal published frameworks (METR, 2025).

The frameworks look different at first glance. They also share a lot underneath. Each one names some class of dangerous capability or harmful outcome. Each commits to evaluations against thresholds. Each specifies mitigations that get triggered when a threshold is crossed. Each describes at least some governance process. So the substance is more similar than the surface suggests. But the surface still matters, because comparing two labs' frameworks today requires reading both from start to finish. The Frontier Model Forum has begun documenting "common elements" (FMF, 2025). METR maintains a primer with the same goal (METR, 2025). Neither project gives you a structured, machine-queryable, version-trackable representation of any single framework, never mind the full population.

Safety Framework Cards close that gap. Each card is a YAML/JSON document a lab publishes alongside its existing framework. The card does not replace the framework. It captures the framework's structural commitments in a controlled vocabulary, and once it exists it can be validated by a public linter, diffed across versions, and rendered for side-by-side cross-lab comparison.

The paper contributes four things. First, a schema (spec v0.1) that covers six structural dimensions with required and recommended fields. Second, an open-source reference implementation, meaning a Python validator, an HTML renderer, and a static GitHub Pages site. Third, nine reference cards — eight retrofits of currently-published frameworks and one card documenting Mistral's non-publication as a structural finding in its own right. Fourth, an empirical analysis of the resulting cards, which surfaces three convergences, four divergences, and one universal disclosure gap.

Positioning-wise, this is a Model Cards-shaped intervention. Model Cards (Mitchell et al., 2019) and Datasheets for Datasets (Gebru et al., 2021) are the direct precedents. Both proposed a standardized artifact backed by a structural rationale, shipped a reference implementation, and then let industry adoption follow. The playbook works for high-stakes documentation artifacts, and I think frontier safety frameworks are exactly that.

## 2. Background and Related Work

### 2.1 Frontier AI safety frameworks

By a *frontier safety framework* I mean a public, model-developer-issued document that specifies four things: the capability levels or harm outcomes the developer treats as requiring elevated handling; the evaluations that determine whether a given model has those capabilities; the mitigations triggered when a threshold is crossed; and the governance process around those decisions. As of May 2026, eight major frontier labs have published such frameworks. METR's December 2025 review adds Magic, Naver, G42, and NVIDIA to the list, bringing the total to twelve. Several Seoul-summit signatories, notably Mistral, have not published yet.

The first-generation frameworks — Anthropic's RSP, OpenAI's Preparedness Framework, and DeepMind's FSF — have iterated substantially. Anthropic's v3.0 (February 2026) was a rewrite that decoupled "ASL" from model identity (it now refers to groups of safeguards, not to individual models) and introduced Capability Thresholds, Required Safeguards, Frontier Safety Roadmaps, and quarterly Risk Reports. OpenAI's v2 (April 2025) removed persuasion from the Tracked Categories, narrowed CBRN to Biological and Chemical (with Nuclear and Radiological moved to Research Categories), and added AI Self-improvement. DeepMind's v3 (September 2025) added manipulation and shutdown-resistance CCLs on top of the v2 CBRN/cyber/ML-R&D set.

Second-generation frameworks from Meta, Amazon, Microsoft, Cohere, and xAI vary more. Meta's is harm-outcome-based rather than capability-tiered. xAI's is benchmark-driven and has received substantial public criticism from safety researchers. Cohere's emphasizes enterprise/domain-specific risks alongside catastrophic risk.

### 2.2 Existing comparative work

Three lines of comparative work already exist. The Frontier Model Forum publishes a Technical Report Series that includes "Risk Taxonomy and Thresholds for Frontier AI Frameworks" and "Managing Advanced Cyber Risks in Frontier AI Frameworks." These reports classify *risks* (CBRN, cyber, autonomy) and the thresholds at which each becomes acute. They are written collectively by member labs and are not peer-reviewed. METR maintains a "Common Elements of Frontier AI Safety Policies" primer (most recent update December 2025) that summarizes shared structural elements across the twelve labs with published policies. Informal commercial overviews compare frameworks side by side at a non-technical level.

None of the three lines does what this paper does: provide a structured, machine-readable specification with a public validator and renderer that can be applied uniformly across labs and revisions.

### 2.3 Standardized-artifact precedents

Several academic papers have shifted industry practice by proposing a standardized documentation artifact: Model Cards (Mitchell et al., 2019), Datasheets for Datasets (Gebru et al., 2021), Data Cards (Pushkarna et al., 2022), Reward Reports (Gilbert et al., 2023), and System Cards (OpenAI, 2023; Anthropic, 2024). Safety Framework Cards fit in that lineage.

---

## 3. The Schema

The schema decomposes a framework along six dimensions, one for each of the questions any framework must eventually answer end-to-end.

**D1. Risk Ontology.** Which harms are in scope. Sub-axes: `scope_basis` (capability_based, harm_based, hybrid); `in_scope_harms` (controlled vocabulary); `enumeration_type` (open or closed); optional severity definitions.

**D2. Capability Thresholds.** How dangerous-capability levels get operationalized. Sub-axes: `threshold_model` (discrete_tiers, continuous_score, hybrid); tier taxonomy; `measurement_basis` (uplift_relative, absolute, hybrid); pre- vs. post-mitigation framing.

**D3. Evaluation Methodology.** What evidence determines whether a threshold has been crossed. Sub-axes: `eval_sources` (internal, third_party, government_AISI, academic, external_red_team); named third parties; eval types; cadence; reproducibility commitments.

**D4. Mitigation Commitments.** What responses get triggered. Sub-axes: technical mitigations, access controls, operational measures, halting triggers, reversibility.

**D5. Governance Triggers.** Who decides and how. Sub-axes: decision body, pre_committed vs. discretionary, external review, public disclosure, whistleblower protections.

**D6. Revision Protocol.** How the framework itself changes. Sub-axes: cadence; ratchet direction (tightening_only, bidirectional, unspecified); public_diff_required; sunset clauses.

Why six, and why these six? The pipeline is not arbitrary. Risk ontology has to come first, because you cannot quantize what you have not bounded. Thresholds have to come next, because you cannot measure what you have not defined. Evaluations feed mitigations, mitigations feed governance, and revision protocol is meta to everything else. The dimension count follows from that reading. Sub-axes were chosen empirically: I iterated between the schema and the eight retrofit attempts described in Section 5, keeping the sub-axes where labs actually diverge and dropping the ones where all labs looked the same.

---

## 4. Reference Implementation

The reference implementation ships under MIT license. Three components.

**Validator** (`safety-card lint <card.yaml>`). Checks the card against the JSON Schema (Draft 2020-12, with backward compatibility to Draft 7). Reports missing required fields, controlled-vocabulary violations, and structural malformation. Adds a weighted completeness score against recommended fields, plus six cross-field consistency warnings.

**Renderer** (`render.py`). Produces per-card HTML pages, a side-by-side comparison view across all cards, and a versioned diff between two versions of the same lab's card. Static output, deployable to GitHub Pages as-is.

**Reference cards.** Nine YAML files retrofitting public frameworks against the schema. Eight are positive worked examples; the ninth (Mistral) documents non-publication as a structural finding.

A lab adopting the workflow forks the repo, fills in `schema/template.yaml`, runs the validator, and renders to HTML. In my own testing, an unfamiliar framework takes about thirty minutes end-to-end.

---

## 5. Empirical Findings

The nine cards are marked `verification_status: self_verified` pending publisher confirmation.

### 5.1 Completeness scores

Running the validator against the nine cards produces completeness scores (recommended-field coverage) as follows:

| Lab | Framework | Version | Completeness |
|---|---|---|---|
| Anthropic | Responsible Scaling Policy | v3.1 (Apr 2026) | 100.0% |
| OpenAI | Preparedness Framework | v2.0 (Apr 2025) | 97.4% |
| Google DeepMind | Frontier Safety Framework | v3.0 (Sep 2025) | 94.7% |
| Amazon | Frontier Model Safety Framework | v2.7 (Feb 2025) | 84.2% |
| Microsoft | Frontier Governance Framework | v1.0 (Feb 2025) | 84.2% |
| Meta | Frontier AI Framework | v1.0 (Feb 2025) | 81.6% |
| Cohere | Secure AI Frontier Model Framework | v1.0 (Feb 2025) | 76.3% |
| xAI | Risk Management Framework | v1.0 (Aug 2025) | 57.9% |
| Mistral | (no published framework) | n/a | 39.5% |

The scores cluster in three tiers: first-generation frameworks above 94%, mid-tier publishers between 76% and 84%, and unpublished or under-specified frameworks below 60%. This is not a ranking of safety performance. It is a measure of how much of the structural spec the public disclosure actually fills in. The variance is the finding.

### 5.2 Three convergences

**C1. Capability-based scoping.** Seven of the eight published frameworks score `capability_based` on D1. Meta is the sole outlier, with `harm_based` scoping. Across all eight, CBRN or biological uplift and cyber appear as in-scope harms.

**C2. Internal plus external evaluation, with named third parties at the top tier.** Eight frameworks list `internal` as an evaluation source. The three first-generation labs (Anthropic, OpenAI, DeepMind) go further, naming specific external evaluators — METR, Apollo Research, UK AISI, US AISI — and treating external capability evaluation as `required`.

**C3. Pre-deployment evaluation is `required`.** Seven of the eight published frameworks treat pre-deployment evaluation as required. xAI scores it as `recommended`, which the validator flags as a gap relative to the peer group.

### 5.3 Four divergences

**D1. Capability-based vs. harm-based scoping.** Meta alone treats outcomes and harms as the primary trigger, rather than capability levels. The schema handles both paradigms via `scope_basis`.

**D2. Pre- vs. post-mitigation measurement.** Only OpenAI's framework tracks both pre- and post-mitigation thresholds. Everyone else measures pre-mitigation only.

**D3. Tier structure.** Anthropic uses Capability Thresholds keyed to harm domains with ASL safeguard groups. DeepMind uses Critical Capability Levels per harm domain (Bio, Cyber, ML R&D, Manipulation, Shutdown in v3). OpenAI uses four severity tiers (Low, Medium, High, Critical). Meta uses two outcome tiers (High, Critical). Microsoft also uses four tiers. xAI uses continuous scores without discrete tiers. The schema's `tier_taxonomy` field handles all of these, but the underlying variation is irreducible.

**D4. Ratchet direction.** Anthropic explicitly commits to `tightening_only` revisions. OpenAI's v1-to-v2 update removed persuasion entirely, which is a structural loosening. That classifies OpenAI's framework as `bidirectional`. Most second-generation frameworks leave the ratchet axis `unspecified`. The takeaway is that the field has not yet converged on a tightening-only norm.

### 5.4 One universal gap

**G1. Third-party verification of evaluations.** No framework in the corpus commits to fully reproducible third-party verification of capability evaluations. Third parties are *engaged* (D3's `named_third_parties` field is populated for the first-generation labs), but the evaluations themselves are not fully reproducible. `eval_scripts_published` is false across every framework. `benchmarks_published` is false across every framework. Even where methodologies are described, third parties cannot audit independently. This is the most striking structural-disclosure gap the spec exposes, and it is a natural target for regulatory or FMF-coordinated intervention.

### 5.5 The non-publication case (Mistral)

Mistral AI signed the May 2024 AI Seoul Summit Frontier AI Safety Commitments. Per METR's December 2025 review, Mistral has not published a formal frontier safety framework. The non-publication shows up in the spec as a near-zero completeness score (39.5%) on a placeholder card. The gap between summit commitment and follow-through is itself something the spec exposes cleanly.

---

## 6. Discussion

A validated population of Safety Framework Cards collapses N×M disclosure asks into one queryable artifact. Regulators can query the population for any structural property the schema captures — third-party review commitments, pre-deployment cadence, named external reviewers — and identify outliers instantly. Emerging labs get scaffolding: a new entrant publishing its first framework can use the recommended-field list as a checklist, and the validator's completeness score gives a rough benchmark against the established peer group. The Frontier Model Forum, whose 2025 Technical Report Series has been moving toward standardization on the risk-taxonomy axis, gets a complementary standardization on the framework-structure axis. Any of these three stakeholders can adopt the spec independently.

**Limitations.** The cards reflect public commitments, not internal practice. `self_verified` is the default status pending publisher confirmation. Frameworks evolve rapidly, and a quarterly versioning cadence at the card level is realistic. The schema itself will iterate; v0.1 is a starting point, not a final standard.

---

## 7. Conclusion

Safety Framework Cards are a Model Cards-shaped adoptable specification for frontier AI safety frameworks. The paper ships the spec, a reference implementation, and a nine-card audit that surfaces three convergences, four divergences, and one universal disclosure gap. The design is additive to existing frameworks, low-cost for labs to fill in, and immediately useful to regulators and emerging labs. Adoption is now the campaign.

---

## Acknowledgments

This work was conducted independently. Datasets used: publicly available safety framework documents from Anthropic, OpenAI, Google DeepMind, Meta, Amazon, Microsoft, Cohere, xAI, and Mistral (via absence). Comparative reference: METR's Common Elements of Frontier AI Safety Policies (Dec 2025) and the Frontier Model Forum's Technical Report Series (2025).

---

## References

Anthropic. (2026). *Responsible Scaling Policy v3.1*. https://www.anthropic.com/responsible-scaling-policy

Frontier Model Forum. (2025a). *Risk Taxonomy and Thresholds for Frontier AI Frameworks*. https://www.frontiermodelforum.org/uploads/2025/06/FMF-Technical-Report-on-Frontier-Risk-Taxonomy-and-Thresholds.pdf

Frontier Model Forum. (2025b). *Managing Advanced Cyber Risks in Frontier AI Frameworks*. https://www.frontiermodelforum.org/technical-reports/managing-advanced-cyber-risks-in-frontier-ai-frameworks/

Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J. W., Wallach, H., Daumé III, H., & Crawford, K. (2021). Datasheets for datasets. *Communications of the ACM*, 64(12), 86–92.

Gilbert, T. K., et al. (2023). Reward Reports for Reinforcement Learning. *AIES 2023*.

Google DeepMind. (2025). *Frontier Safety Framework v3.0*. https://deepmind.google/blog/strengthening-our-frontier-safety-framework/

Meta. (2025). *Frontier AI Framework*. https://ai.meta.com/

METR. (2025). *Common Elements of Frontier AI Safety Policies (December 2025 Update)*. https://metr.org/common-elements

Microsoft. (2025). *Frontier Governance Framework*.

Mitchell, M., Wu, S., Zaldivar, A., et al. (2019). Model cards for model reporting. *FAccT 2019*, 220–229.

OpenAI. (2025). *Preparedness Framework v2*. https://openai.com/index/updating-our-preparedness-framework/

Pushkarna, M., Zaldivar, A., & Kjartansson, O. (2022). Data Cards: Purposeful and Transparent Dataset Documentation for Responsible AI. *FAccT 2022*.

xAI. (2025). *Risk Management Framework*. https://data.x.ai/2025-08-20-xai-risk-management-framework.pdf

---

## Appendix A — Full Schema

See `schema/safety_framework_card.schema.json` in the reference repository.

## Appendix B — Per-Card Notes

See `cards/*.yaml` files in the reference repository. Each card includes field-by-field justification and `open_questions` markers for assertions requiring publisher verification.

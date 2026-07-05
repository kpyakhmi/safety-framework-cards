# Social post templates (Day 7 afternoon, after arXiv goes live)

---

## X / Twitter (single post)

```
new paper + open-source spec: Safety Framework Cards.

a standardized, machine-readable schema for documenting frontier AI safety frameworks (RSPs, Preparedness Frameworks, FSFs).

9 reference cards. python validator. HTML renderer.

arXiv: [link]
repo: [link]
🧵 below ↓
```

**Thread (4 posts):**

```
1/ Anthropic, OpenAI, DeepMind, Meta, Amazon, Microsoft, xAI, Mistral, and Cohere all publish public safety frameworks. Each is published as prose in idiosyncratic structure. Regulators are asking the same question: are they comparable?
```

```
2/ Safety Framework Cards is a Model-Cards-style spec. Six structural dimensions: risk ontology, capability thresholds, eval methodology, mitigations, governance, revision protocol. Machine-readable YAML. Open schema.
```

```
3/ I retrofitted nine public frameworks as cards. Completeness scores (recommended-field coverage) range from 50% (xAI, Mistral) to 100% (Anthropic). 3 convergences, 4 divergences, 1 universal gap surfaced by the spec.
```

```
4/ The universal gap: no framework commits to reproducible third-party verification of capability evaluations. Eval scripts are not published. Benchmarks are not published. This is the most striking structural-disclosure gap in the field.
```

```
5/ The cards are *additive* — labs map their existing frameworks into the schema without rewriting commitments. ~30 minutes per card. Pitching to FMF and lab safety teams this week.

repo: [link]
arxiv: [link]

feedback welcome via issues.
```

---

## LinkedIn (single post)

```
New work: Safety Framework Cards — a standardized specification for documenting frontier AI safety commitments.

Frontier AI labs (Anthropic, OpenAI, Google DeepMind, Meta, Amazon, Microsoft, xAI, Mistral, Cohere) now all publish public safety frameworks — Responsible Scaling Policies, Preparedness Frameworks, Frontier Safety Frameworks, and equivalents. Each is published in prose, in idiosyncratic structure. Regulators (EU AI Office, UK AISI, US NIST AISI, Singapore IMDA), the Frontier Model Forum, partners, and insurers are all asking the same question: are these frameworks comparable?

I propose a Model-Cards-style answer: a machine-readable schema capturing the structural anatomy of a safety framework along six dimensions (risk ontology, capability thresholds, evaluation methodology, mitigation commitments, governance triggers, revision protocol). The cards are *additive* — labs map their existing frameworks into the spec without rewriting commitments.

The paper retrofits nine public frameworks as cards. Three structural convergences, four divergences, and one universal disclosure gap emerge from the comparison. The reference implementation (Python validator, HTML renderer, GitHub Pages site) is open source.

Paper: [arxiv-link]
Repository + reference cards: [github-link]
Rendered comparison view: [github-pages-link]

This is v0.1 of an open specification. Comments welcome via GitHub issues. I am particularly interested in feedback from lab safety teams who would be willing to verify the reference card for their framework.

#AIsafety #AIgovernance #frontierAI #responsibleAI
```

---

## LessWrong / EA Forum

```
Title: Safety Framework Cards: a Model-Cards-style spec for frontier AI safety frameworks

(Cross-posted from arXiv.)

# Summary

I posted a paper today proposing **Safety Framework Cards** — a machine-readable specification (JSON Schema + YAML) for documenting frontier AI safety commitments. Nine reference cards retrofit existing frameworks (Anthropic RSP, OpenAI Preparedness Framework, DeepMind FSF, Meta Outcomes-Led, Amazon FMSF, Microsoft RAI Standard + frontier, xAI, Mistral, Cohere). Open-source validator and HTML renderer included.

# Why this might matter

Frontier safety frameworks have proliferated over the last 18 months but are published in incompatible prose. The FMF and METR have begun documenting "common elements" informally; this work attempts the structured-instrument version. The output is intended for adoption — labs map existing frameworks into the schema in ~30 minutes; the card is published alongside (not replacing) the framework.

# What the comparison surfaces

- 3 convergences (capability-based scoping, internal+external evaluation, required pre-deployment evaluation)
- 4 divergences (capability-vs-harm scoping, pre/post-mitigation, tier structure, ratchet commitments)
- 1 universal gap: no framework commits to reproducible third-party verification of capability evaluations.

# Links

Paper: [arxiv-link]
Repo: [github-link]
Rendered comparison: [github-pages-link]

Comments welcome.
```

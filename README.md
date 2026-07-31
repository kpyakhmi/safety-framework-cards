Safety Framework Cards
A standardized specification for documenting frontier AI safety commitments.
  
Frontier AI labs publish public safety frameworks (Anthropic's RSP, OpenAI's Preparedness Framework, Google DeepMind's FSF, Meta's Outcomes-Led Framework, and others). Each framework is published as prose in idiosyncratic structure. A Safety Framework Card is a machine-readable companion that documents a framework's structural commitments along six dimensions, so regulators, partners, and researchers can compare frameworks systematically.
This is an additive artifact — it does not replace the framework. A lab maps its existing framework into the schema in roughly thirty minutes. The card is then validated, rendered to HTML, and diffed across versions.
Paper (PDF) · Live Cards · Quick Start · License: MIT
________________________________________
Live Demo
Rendered cards and side-by-side comparison view: https://kpyakhmi.github.io/safety-framework-cards/
Lab	Framework	Version
Anthropic	Responsible Scaling Policy	v3.1
OpenAI	Preparedness Framework	v2.0
Google DeepMind	Frontier Safety Framework	v3.0
Amazon	Frontier Model Safety Framework	v2.7
Microsoft	Frontier Governance Framework	v1.0
Meta	Frontier AI Framework (Outcomes-Led)	v1.0
Cohere	Secure AI Frontier Model Framework	v1.0
xAI	Risk Management Framework	v1.0
Mistral	(no published framework)	n/a
→ Side-by-side comparison
________________________________________
What's in this repo
schema/                                  spec v0.1
  safety_framework_card.schema.json      JSON Schema definition
  template.yaml                          blank card template
cards/                                   nine reference cards
  anthropic-rsp.yaml                     Anthropic Responsible Scaling Policy
  openai-preparedness.yaml               OpenAI Preparedness Framework
  deepmind-fsf.yaml                      Google DeepMind Frontier Safety Framework
  meta-outcomes-led.yaml                 Meta Outcomes-Led Framework
  amazon-fmsf.yaml                       Amazon Frontier Model Safety Framework
  microsoft-rais.yaml                    Microsoft Responsible AI Standard + frontier
  xai-commitments.yaml                   xAI public safety commitments
  mistral-policy.yaml                    Mistral AI commitments
  cohere-commitments.yaml                Cohere responsible AI practices
validator/safety_card.py                 Python CLI validator
renderer/render.py                       Python HTML renderer
docs/                                    rendered HTML site (deploy to GitHub Pages)
paper/paper.md                           accompanying paper draft
________________________________________
Quick start
# Install dependencies
pip install pyyaml jsonschema

# Validate a single card
python validator/safety_card.py lint cards/anthropic-rsp.yaml

# Validate every card
python validator/safety_card.py lint cards/

# Render all cards as a static site (index + per-card + comparison view)
python renderer/render.py site cards/ -o docs/

# Render a side-by-side comparison
python renderer/render.py compare cards/anthropic-rsp.yaml cards/openai-preparedness.yaml -o compare.html

# Diff two versions of the same lab's card
python renderer/render.py diff cards/anthropic-rsp-v1.yaml cards/anthropic-rsp-v2.yaml -o diff.html
________________________________________
The six dimensions
A Safety Framework Card captures the structural anatomy of a frontier safety framework along six dimensions corresponding to the questions any framework must answer:
	Dimension	What it captures
D1	Risk Ontology	Which harms the framework names as in-scope (CBRN, cyber, autonomy, etc.)
D2	Capability Thresholds	How dangerous-capability levels are operationalized (tiers, scores)
D3	Evaluation Methodology	What evidence determines threshold crossings (eval sources, types, cadence)
D4	Mitigation Commitments	What responses are triggered (technical, access, operational, halting)
D5	Governance Triggers	Who decides and how (decision body, external review, disclosure)
D6	Revision Protocol	How the framework itself changes (cadence, ratchet, public diff)
Each dimension has 3–7 controlled-vocabulary sub-axes. See schema/safety_framework_card.schema.json for the formal definition.
________________________________________
How to publish a card for your lab
1.	Copy schema/template.yaml to cards/<your-lab>.yaml.
2.	Fill in the metadata header and every required field.
3.	Fill recommended fields where applicable. The validator scores completeness.
4.	Run python validator/safety_card.py lint cards/<your-lab>.yaml and address any warnings.
5.	Set notes.verification_status to publisher_verified when an authorized representative has confirmed the card's accuracy.
6.	Open a pull request, or publish the card in your own repository.
________________________________________
Status
Spec version: 0.1 — initial draft. Public comment is open via GitHub issues.
Reference cards in this repository are marked verification_status: draft pending publisher confirmation. Cards are based on public framework documents and should not be cited as authoritative until verified by the publishing lab. Each card's notes.open_questions field flags assertions requiring confirmation.
________________________________________
Citation
If you cite this work, please use:
@misc{safety-framework-cards-2026,
  title  = {Safety Framework Cards: A Standardized Specification for Documenting Frontier AI Safety Commitments},
  author = {Kanupriya Yakhmi},
  year   = {2026},
  note   = {Available at https://github.com/kpyakhmi/safety-framework-cards},
}
________________________________________
Contributing
This is an early-stage open specification. We welcome:
•	Lab-published cards for any frontier framework, with publisher_verified status.
•	Schema feedback via GitHub issues. v0.2 will incorporate community feedback after a 30-day comment period.
•	Independent verification of any reference card. PRs that update a card with verified information are particularly welcome.
•	Translation or rendering tools building on the schema.
________________________________________
License
MIT — see LICENSE.
The schema and code are MIT-licensed. Individual reference cards may carry their own license (typically CC-BY-4.0) as declared in the card's metadata.license field. The underlying framework documents remain the intellectual property of the publishing labs.
________________________________________
Acknowledgments
Independent work. Grateful to the frontier-lab safety teams and the METR, Apollo, GovAI, and FMF communities whose public documents and comparative reviews made this synthesis possible. Individual acknowledgments will be added as reference cards are verified by their publishing labs.


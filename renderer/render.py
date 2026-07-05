#!/usr/bin/env python3
"""
render - HTML renderer for Safety Framework Cards (spec v0.1).

Usage:
    python render.py one    <card.yaml> -o out.html
    python render.py site   cards/ -o site/                 # index + per-card + compare
    python render.py compare card_a.yaml card_b.yaml -o compare.html
    python render.py diff    cardA_v1.yaml cardA_v2.yaml -o diff.html
"""

import argparse
import html
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("error: pyyaml required. pip install pyyaml\n")
    sys.exit(2)


CSS = """
:root { --bg:#fafafa; --fg:#111; --muted:#666; --line:#ddd; --accent:#1f3a5f; --warn:#b54708; --good:#067647; }
* { box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
       background: var(--bg); color: var(--fg); margin: 0; line-height: 1.55; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 32px 24px 80px; }
.header { border-bottom: 1px solid var(--line); padding-bottom: 18px; margin-bottom: 28px; }
.header h1 { margin: 0 0 6px; font-size: 26px; color: var(--accent); }
.header .meta { color: var(--muted); font-size: 14px; }
.dim { margin-bottom: 28px; }
.dim h2 { font-size: 17px; color: var(--accent); border-bottom: 1px solid var(--line);
          padding-bottom: 6px; margin: 0 0 10px; }
.row { display: grid; grid-template-columns: 220px 1fr; gap: 12px; padding: 6px 0;
       border-bottom: 1px dotted #eee; font-size: 14px; }
.row.k { color: var(--muted); }
.tag { display: inline-block; padding: 2px 8px; margin: 2px 4px 2px 0; border-radius: 12px;
       background: #eef2f6; color: var(--accent); font-size: 12px; }
.tag.warn { background: #fff5e6; color: var(--warn); }
.tag.good { background: #ecf7ef; color: var(--good); }
.muted { color: var(--muted); font-style: italic; }
.section-empty { color: var(--muted); font-style: italic; padding: 4px 0; }
table.cmp { border-collapse: collapse; width: 100%; font-size: 13px; margin-top: 12px; }
table.cmp th, table.cmp td { border: 1px solid var(--line); padding: 8px 10px; vertical-align: top;
                              text-align: left; }
table.cmp th { background: var(--accent); color: #fff; }
table.cmp td.empty { color: var(--muted); font-style: italic; }
.tier { border: 1px solid var(--line); padding: 10px 12px; margin: 6px 0; background: #fff; border-radius: 4px; }
.tier .id { font-weight: 600; color: var(--accent); }
.footer { color: var(--muted); font-size: 12px; margin-top: 60px; border-top: 1px solid var(--line);
          padding-top: 14px; }
.diff-add { background: #ecf7ef; }
.diff-rem { background: #fbeaea; text-decoration: line-through; }
.idx { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 14px; }
.idx .card { border: 1px solid var(--line); background: #fff; padding: 14px; border-radius: 4px; }
.idx .card a { color: var(--accent); text-decoration: none; font-weight: 600; }
.idx .card .score { color: var(--muted); font-size: 13px; margin-top: 4px; }
"""


def esc(s):
    if s is None:
        return ""
    return html.escape(str(s))


def fmt_list(v):
    if not v:
        return '<span class="muted">(none)</span>'
    return "".join('<span class="tag">{}</span>'.format(esc(x)) for x in v)


def fmt_bool(v):
    if v is True:
        return '<span class="tag good">true</span>'
    if v is False:
        return '<span class="tag warn">false</span>'
    return '<span class="muted">(unset)</span>'


def fmt_val(v):
    if v is None or v == "":
        return '<span class="muted">(unset)</span>'
    if isinstance(v, list):
        return fmt_list(v)
    if isinstance(v, bool):
        return fmt_bool(v)
    if isinstance(v, dict):
        # leave dict rendering to caller
        return '<pre style="font-size:12px">{}</pre>'.format(esc(json.dumps(v, indent=2)))
    return esc(v)


def row(k, v):
    return '<div class="row"><div class="k">{}</div><div>{}</div></div>'.format(esc(k), v if isinstance(v, str) and v.startswith("<") else fmt_val(v))


def render_tiers(tiers):
    if not tiers:
        return '<div class="section-empty">No tiers declared</div>'
    out = []
    for t in tiers:
        out.append('<div class="tier"><span class="id">{}</span> &mdash; {}'.format(
            esc(t.get("tier_id", "?")),
            esc(t.get("name", ""))
        ))
        if t.get("capability_definition"):
            out.append('<div style="margin-top:4px;font-size:13px">{}</div>'.format(esc(t["capability_definition"])))
        if t.get("indicators"):
            out.append('<div style="margin-top:6px"><span class="k">indicators:</span> {}</div>'.format(fmt_list(t["indicators"])))
        if t.get("triggered_mitigations"):
            out.append('<div><span class="k">mitigations:</span> {}</div>'.format(fmt_list(t["triggered_mitigations"])))
        out.append('</div>')
    return "".join(out)


def render_card(card):
    md = card.get("metadata", {})
    d1 = card.get("d1_risk_ontology", {})
    d2 = card.get("d2_capability_thresholds", {})
    d3 = card.get("d3_evaluation_methodology", {})
    d4 = card.get("d4_mitigation_commitments", {})
    d5 = card.get("d5_governance_triggers", {})
    d6 = card.get("d6_revision_protocol", {})
    notes = card.get("notes", {})

    parts = []
    parts.append('<div class="header">')
    parts.append('<h1>{}</h1>'.format(esc(md.get("framework_name", "(untitled)"))))
    parts.append('<div class="meta">Published by <strong>{}</strong> &middot; version <strong>{}</strong> &middot; effective {}'.format(
        esc(md.get("publisher", "?")), esc(md.get("version", "?")), esc(md.get("effective_date", "?"))
    ))
    if md.get("canonical_url"):
        parts.append(' &middot; <a href="{}">canonical</a>'.format(esc(md["canonical_url"])))
    parts.append('</div>')
    if notes.get("verification_status") == "draft":
        parts.append('<div style="margin-top:8px"><span class="tag warn">DRAFT - not publisher-verified</span></div>')
    parts.append('</div>')

    # D1
    parts.append('<div class="dim"><h2>D1. Risk Ontology</h2>')
    parts.append(row("scope_basis", d1.get("scope_basis")))
    parts.append(row("in_scope_harms", d1.get("in_scope_harms")))
    parts.append(row("enumeration_type", d1.get("enumeration_type")))
    if d1.get("severity_definitions"):
        rows = []
        for s in d1["severity_definitions"]:
            rows.append('<div><strong>{}</strong>: {}</div>'.format(
                esc(s.get("level", "?")), esc(s.get("definition", ""))))
        parts.append(row("severity_definitions", "".join(rows)))
    parts.append('</div>')

    # D2
    parts.append('<div class="dim"><h2>D2. Capability Thresholds</h2>')
    parts.append(row("threshold_model", d2.get("threshold_model")))
    parts.append(row("measurement_basis", d2.get("measurement_basis")))
    parts.append(row("pre_or_post_mitigation", d2.get("pre_or_post_mitigation")))
    parts.append(row("tier_taxonomy", render_tiers(d2.get("tier_taxonomy") or [])))
    parts.append('</div>')

    # D3
    parts.append('<div class="dim"><h2>D3. Evaluation Methodology</h2>')
    parts.append(row("eval_sources", d3.get("eval_sources")))
    parts.append(row("named_third_parties", d3.get("named_third_parties")))
    parts.append(row("eval_types", d3.get("eval_types")))
    cad = d3.get("cadence", {})
    parts.append(row("cadence (pre-deployment)", cad.get("pre_deployment")))
    parts.append(row("cadence (continuous)", cad.get("continuous")))
    parts.append(row("cadence (pre-training)", cad.get("pre_training_decision")))
    rp = d3.get("reproducibility", {})
    parts.append(row("methods_published", rp.get("methods_published")))
    parts.append(row("benchmarks_published", rp.get("benchmarks_published")))
    parts.append(row("eval_scripts_published", rp.get("eval_scripts_published")))
    parts.append(row("results_published", rp.get("results_published")))
    parts.append('</div>')

    # D4
    parts.append('<div class="dim"><h2>D4. Mitigation Commitments</h2>')
    parts.append(row("technical", d4.get("technical")))
    parts.append(row("access_controls", d4.get("access_controls")))
    parts.append(row("operational", d4.get("operational")))
    parts.append(row("halting_triggers", d4.get("halting_triggers")))
    rv = d4.get("reversibility", {})
    parts.append(row("mitigation_lift_protocol", rv.get("mitigation_lift_protocol")))
    parts.append(row("rollback_capability", rv.get("rollback_capability")))
    parts.append('</div>')

    # D5
    parts.append('<div class="dim"><h2>D5. Governance Triggers</h2>')
    db = d5.get("decision_body", {})
    parts.append(row("decision_body (threshold)", db.get("threshold_assessment")))
    parts.append(row("decision_body (deployment)", db.get("deployment_above_tier")))
    parts.append(row("decision_body (revisions)", db.get("framework_revision")))
    parts.append(row("pre_commitment_vs_discretion", d5.get("pre_commitment_vs_discretion")))
    er = d5.get("external_review", {})
    parts.append(row("external_review (capability_evals)", er.get("capability_evals")))
    parts.append(row("external_review (revisions)", er.get("framework_revisions")))
    parts.append(row("named_external_reviewers", er.get("named_external_reviewers")))
    pd = d5.get("public_disclosure", {})
    parts.append(row("disclosure (crossings)", pd.get("threshold_crossings")))
    parts.append(row("disclosure (failures)", pd.get("mitigation_failures")))
    parts.append(row("disclosure timeline", pd.get("timeline_to_disclose")))
    wb = d5.get("whistleblower_protections", {})
    parts.append(row("whistleblower policy", wb.get("policy_exists")))
    parts.append(row("external reporting channel", wb.get("external_reporting_channel")))
    parts.append('</div>')

    # D6
    parts.append('<div class="dim"><h2>D6. Revision Protocol</h2>')
    parts.append(row("cadence", d6.get("cadence")))
    parts.append(row("ratchet_commitment", d6.get("ratchet_commitment")))
    parts.append(row("public_diff_required", d6.get("public_diff_required")))
    parts.append(row("public_comment_period", d6.get("public_comment_period")))
    sc = d6.get("sunset_clauses", {})
    parts.append(row("sunset (capabilities)", sc.get("capability_definitions")))
    parts.append(row("sunset (mitigations)", sc.get("mitigation_specifics")))
    parts.append('</div>')

    return "\n".join(parts)


def html_page(title, body, extra_css=""):
    return ("<!doctype html><html><head><meta charset='utf-8'>"
            "<title>{title}</title><style>{css}{extra}</style></head>"
            "<body><div class='wrap'>{body}"
            "<div class='footer'>Generated by safety-framework-cards renderer &middot; spec v0.1</div>"
            "</div></body></html>").format(title=esc(title), css=CSS, extra=extra_css, body=body)


# ---------------- comparison ----------------

COMPARE_FIELDS = [
    ("D1 scope_basis", "d1_risk_ontology.scope_basis"),
    ("D1 in-scope harms", "d1_risk_ontology.in_scope_harms"),
    ("D1 enumeration", "d1_risk_ontology.enumeration_type"),
    ("D2 threshold_model", "d2_capability_thresholds.threshold_model"),
    ("D2 measurement_basis", "d2_capability_thresholds.measurement_basis"),
    ("D2 pre/post mitigation", "d2_capability_thresholds.pre_or_post_mitigation"),
    ("D3 eval_sources", "d3_evaluation_methodology.eval_sources"),
    ("D3 named third-parties", "d3_evaluation_methodology.named_third_parties"),
    ("D3 pre-deployment cadence", "d3_evaluation_methodology.cadence.pre_deployment"),
    ("D3 continuous cadence", "d3_evaluation_methodology.cadence.continuous"),
    ("D3 methods published", "d3_evaluation_methodology.reproducibility.methods_published"),
    ("D4 technical mitigations", "d4_mitigation_commitments.technical"),
    ("D4 access controls", "d4_mitigation_commitments.access_controls"),
    ("D4 halting triggers", "d4_mitigation_commitments.halting_triggers"),
    ("D5 pre_commit vs discretion", "d5_governance_triggers.pre_commitment_vs_discretion"),
    ("D5 external review (evals)", "d5_governance_triggers.external_review.capability_evals"),
    ("D5 disclosure (crossings)", "d5_governance_triggers.public_disclosure.threshold_crossings"),
    ("D5 whistleblower policy", "d5_governance_triggers.whistleblower_protections.policy_exists"),
    ("D6 cadence", "d6_revision_protocol.cadence"),
    ("D6 ratchet", "d6_revision_protocol.ratchet_commitment"),
    ("D6 public diff", "d6_revision_protocol.public_diff_required"),
]


def get_path(obj, path):
    cur = obj
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None
    return cur


def fmt_cmp(v):
    if v is None or v == "":
        return ('<td class="empty">(unset)</td>')
    if isinstance(v, list):
        if not v:
            return '<td class="empty">(none)</td>'
        return "<td>" + ", ".join(esc(x) for x in v) + "</td>"
    if isinstance(v, bool):
        return "<td>{}</td>".format("yes" if v else "no")
    return "<td>{}</td>".format(esc(v))


def render_compare(cards):
    head = "<tr><th>Dimension / Field</th>" + "".join(
        "<th>{}<br><small>{}</small></th>".format(
            esc(c.get("metadata", {}).get("publisher", "?")),
            esc(c.get("metadata", {}).get("version", "?"))
        ) for c in cards) + "</tr>"
    rows = []
    for label, path in COMPARE_FIELDS:
        cells = "".join(fmt_cmp(get_path(c, path)) for c in cards)
        rows.append("<tr><td><strong>{}</strong></td>{}</tr>".format(esc(label), cells))
    return "<table class='cmp'>" + head + "".join(rows) + "</table>"


def render_diff(a, b):
    """Side-by-side diff between two versions of the same lab's card."""
    rows = []
    for label, path in COMPARE_FIELDS:
        va = get_path(a, path)
        vb = get_path(b, path)
        same = va == vb
        cell_a = fmt_cmp(va).replace("<td", "<td class='diff-rem'", 1) if not same else fmt_cmp(va)
        cell_b = fmt_cmp(vb).replace("<td", "<td class='diff-add'", 1) if not same else fmt_cmp(vb)
        rows.append("<tr><td><strong>{}</strong></td>{}{}</tr>".format(esc(label), cell_a, cell_b))
    head = "<tr><th>Field</th><th>{} v{}</th><th>{} v{}</th></tr>".format(
        esc(a.get("metadata", {}).get("publisher", "?")),
        esc(a.get("metadata", {}).get("version", "?")),
        esc(b.get("metadata", {}).get("publisher", "?")),
        esc(b.get("metadata", {}).get("version", "?")),
    )
    return "<table class='cmp'>" + head + "".join(rows) + "</table>"


def render_index(cards_info):
    body = ['<div class="header"><h1>Safety Framework Cards &mdash; index</h1>'
            '<div class="meta">Generated index of all rendered cards.</div></div>',
            '<div class="idx">']
    for info in cards_info:
        body.append(('<div class="card"><a href="{href}">{name}</a>'
                     '<div class="score">Publisher: {pub} &middot; version {ver}</div></div>').format(
            href=esc(info["href"]),
            name=esc(info["name"]),
            pub=esc(info["publisher"]),
            ver=esc(info["version"]),
        ))
    body.append('</div>')
    body.append('<p style="margin-top:24px">&middot; <a href="compare.html">Side-by-side comparison</a></p>')
    return "\n".join(body)


def load(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def main():
    ap = argparse.ArgumentParser(prog="render")
    sub = ap.add_subparsers(dest="cmd")

    p_one = sub.add_parser("one")
    p_one.add_argument("card")
    p_one.add_argument("-o", "--output", default="card.html")

    p_cmp = sub.add_parser("compare")
    p_cmp.add_argument("cards", nargs="+")
    p_cmp.add_argument("-o", "--output", default="compare.html")

    p_diff = sub.add_parser("diff")
    p_diff.add_argument("card_a")
    p_diff.add_argument("card_b")
    p_diff.add_argument("-o", "--output", default="diff.html")

    p_site = sub.add_parser("site")
    p_site.add_argument("dir")
    p_site.add_argument("-o", "--output", default="site")

    args = ap.parse_args()

    if args.cmd == "one":
        c = load(args.card)
        title = c.get("metadata", {}).get("framework_name", "Safety Framework Card")
        body = render_card(c)
        Path(args.output).write_text(html_page(title, body), encoding="utf-8")
        print("Wrote {}".format(args.output))
        return 0

    if args.cmd == "compare":
        cards = [load(p) for p in args.cards]
        body = "<div class='header'><h1>Safety Framework Cards &mdash; comparison</h1></div>" + render_compare(cards)
        Path(args.output).write_text(html_page("Comparison", body), encoding="utf-8")
        print("Wrote {}".format(args.output))
        return 0

    if args.cmd == "diff":
        a = load(args.card_a)
        b = load(args.card_b)
        body = "<div class='header'><h1>Safety Framework Card &mdash; version diff</h1></div>" + render_diff(a, b)
        Path(args.output).write_text(html_page("Diff", body), encoding="utf-8")
        print("Wrote {}".format(args.output))
        return 0

    if args.cmd == "site":
        out = Path(args.output)
        out.mkdir(parents=True, exist_ok=True)
        cards = []
        for p in sorted(Path(args.dir).glob("*.yaml")):
            c = load(p)
            html_name = p.stem + ".html"
            body = render_card(c)
            title = c.get("metadata", {}).get("framework_name", p.stem)
            (out / html_name).write_text(html_page(title, body), encoding="utf-8")
            cards.append((c, html_name))

        # compare
        body = "<div class='header'><h1>All cards &mdash; side-by-side</h1></div>" + render_compare([c for c, _ in cards])
        (out / "compare.html").write_text(html_page("Compare all cards", body), encoding="utf-8")

        # index
        info = [{
            "href": h,
            "name": c.get("metadata", {}).get("framework_name", h),
            "publisher": c.get("metadata", {}).get("publisher", ""),
            "version": c.get("metadata", {}).get("version", ""),
        } for c, h in cards]
        (out / "index.html").write_text(html_page("Safety Framework Cards", render_index(info)), encoding="utf-8")
        print("Wrote {} cards + index + compare to {}".format(len(cards), out))
        return 0

    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())

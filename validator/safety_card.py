#!/usr/bin/env python3
"""
safety-card - validator for Safety Framework Cards (spec v0.1).

Usage:
    python safety_card.py lint <card.yaml> [<card2.yaml> ...]
    python safety_card.py lint cards/                          # lint every yaml in dir
    python safety_card.py lint card.yaml --format json         # JSON output

Exit codes:
    0 - all cards pass schema validation
    1 - one or more cards fail schema validation
    2 - usage / file error
"""

import argparse
import json
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.stderr.write("error: pyyaml is required. Install: pip install pyyaml jsonschema\n")
    sys.exit(2)

try:
    import jsonschema
    try:
        from jsonschema import Draft202012Validator as _Validator
    except ImportError:
        try:
            from jsonschema import Draft7Validator as _Validator
        except ImportError:
            from jsonschema import Draft4Validator as _Validator
except ImportError:
    sys.stderr.write("error: jsonschema is required. Install: pip install jsonschema\n")
    sys.exit(2)


SCHEMA_PATH_DEFAULT = Path(__file__).parent.parent / "schema" / "safety_framework_card.schema.json"

RECOMMENDED_FIELDS = [
    ("metadata.supersedes", 1),
    ("metadata.contact", 1),
    ("metadata.license", 1),
    ("d1_risk_ontology.severity_definitions", 2),
    ("d2_capability_thresholds.tier_taxonomy", 3),
    ("d3_evaluation_methodology.named_third_parties", 2),
    ("d3_evaluation_methodology.cadence.pre_training_decision", 1),
    ("d3_evaluation_methodology.reproducibility.benchmarks_published", 1),
    ("d3_evaluation_methodology.reproducibility.eval_scripts_published", 1),
    ("d3_evaluation_methodology.reproducibility.results_published", 1),
    ("d4_mitigation_commitments.technical", 2),
    ("d4_mitigation_commitments.access_controls", 2),
    ("d4_mitigation_commitments.operational", 2),
    ("d4_mitigation_commitments.halting_triggers", 2),
    ("d4_mitigation_commitments.reversibility.mitigation_lift_protocol", 1),
    ("d4_mitigation_commitments.reversibility.rollback_capability", 1),
    ("d5_governance_triggers.decision_body.threshold_assessment", 1),
    ("d5_governance_triggers.decision_body.deployment_above_tier", 1),
    ("d5_governance_triggers.decision_body.framework_revision", 1),
    ("d5_governance_triggers.external_review.framework_revisions", 1),
    ("d5_governance_triggers.external_review.named_external_reviewers", 2),
    ("d5_governance_triggers.public_disclosure.mitigation_failures", 1),
    ("d5_governance_triggers.public_disclosure.timeline_to_disclose", 1),
    ("d5_governance_triggers.whistleblower_protections.policy_exists", 1),
    ("d5_governance_triggers.whistleblower_protections.external_reporting_channel", 1),
    ("d6_revision_protocol.public_diff_required", 1),
    ("d6_revision_protocol.public_comment_period", 1),
    ("d6_revision_protocol.sunset_clauses.capability_definitions", 1),
    ("d6_revision_protocol.sunset_clauses.mitigation_specifics", 1),
]


def get_by_path(obj, path):
    cur = obj
    for k in path.split("."):
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return False, None
    return True, cur


def is_filled(value):
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() != ""
    if isinstance(value, (list, dict)):
        return len(value) > 0
    return True


def completeness_score(card):
    achieved = 0
    total = 0
    for path, weight in RECOMMENDED_FIELDS:
        total += weight
        found, value = get_by_path(card, path)
        if found and is_filled(value):
            achieved += weight
    pct = (achieved / total * 100.0) if total else 0.0
    return achieved, total, pct


def cross_field_warnings(card):
    warnings = []

    found_review, review_val = get_by_path(card, "d5_governance_triggers.external_review.capability_evals")
    found_parties, parties_val = get_by_path(card, "d3_evaluation_methodology.named_third_parties")
    if found_review and review_val == "required" and (not found_parties or not is_filled(parties_val)):
        warnings.append("[D5<->D3] External review of capability evals is 'required' but D3 names no third-party evaluators.")

    found_tm, tm_val = get_by_path(card, "d2_capability_thresholds.threshold_model")
    found_tt, tt_val = get_by_path(card, "d2_capability_thresholds.tier_taxonomy")
    if found_tm and tm_val in ("discrete_tiers", "hybrid"):
        if not found_tt or not is_filled(tt_val):
            warnings.append("[D2] threshold_model is '{}' but tier_taxonomy is empty.".format(tm_val))

    found_d, d_val = get_by_path(card, "d5_governance_triggers.public_disclosure.threshold_crossings")
    found_t, t_val = get_by_path(card, "d5_governance_triggers.public_disclosure.timeline_to_disclose")
    if found_d and d_val == "required" and (not found_t or not is_filled(t_val)):
        warnings.append("[D5] Public disclosure of threshold crossings is 'required' but no timeline is specified.")

    found_r, r_val = get_by_path(card, "d6_revision_protocol.ratchet_commitment")
    found_pd, pd_val = get_by_path(card, "d6_revision_protocol.public_diff_required")
    if found_r and r_val == "tightening_only" and not pd_val:
        warnings.append("[D6] ratchet_commitment is 'tightening_only' but public_diff_required is not asserted.")

    found_mp, mp_val = get_by_path(card, "d3_evaluation_methodology.reproducibility.methods_published")
    found_lp, lp_val = get_by_path(card, "d4_mitigation_commitments.reversibility.mitigation_lift_protocol")
    if found_mp and mp_val is False and (not found_lp or lp_val != "not_defined"):
        warnings.append("[D3<->D4] Evaluation methods are unpublished - mitigation_lift_protocol may not be externally verifiable.")

    found_vs, vs_val = get_by_path(card, "notes.verification_status")
    if found_vs and vs_val == "draft":
        warnings.append("[notes] verification_status is 'draft' - confirm with the publishing lab before treating as authoritative.")

    return warnings


def lint_one(path, schema):
    result = {
        "path": str(path),
        "schema_valid": False,
        "schema_errors": [],
        "completeness": {"achieved": 0, "total": 0, "pct": 0.0},
        "warnings": [],
        "summary": "",
    }
    try:
        with open(path, "r", encoding="utf-8") as f:
            card = yaml.safe_load(f)
    except Exception as e:
        result["schema_errors"].append("YAML load failed: {}".format(e))
        result["summary"] = "FAIL - could not parse YAML"
        return result

    validator = _Validator(schema)
    errors = sorted(validator.iter_errors(card), key=lambda e: list(e.path))
    if errors:
        result["schema_valid"] = False
        for e in errors:
            loc = "/".join(str(p) for p in e.path) or "(root)"
            result["schema_errors"].append("{}: {}".format(loc, e.message))
        result["summary"] = "FAIL - schema errors: {}".format(len(errors))
    else:
        result["schema_valid"] = True
        result["summary"] = "OK"

    achieved, total, pct = completeness_score(card)
    result["completeness"] = {"achieved": achieved, "total": total, "pct": round(pct, 1)}
    result["warnings"] = cross_field_warnings(card)
    return result


def collect_paths(args):
    paths = []
    for arg in args:
        p = Path(arg)
        if p.is_dir():
            paths.extend(sorted(p.glob("*.yaml")) + sorted(p.glob("*.yml")))
        elif p.is_file():
            paths.append(p)
        else:
            sys.stderr.write("warning: not found: {}\n".format(arg))
    return paths


def main():
    ap = argparse.ArgumentParser(prog="safety-card")
    sub = ap.add_subparsers(dest="cmd")

    lint = sub.add_parser("lint", help="Validate one or more cards.")
    lint.add_argument("paths", nargs="+", help="YAML file(s) or directory.")
    lint.add_argument("--schema", default=str(SCHEMA_PATH_DEFAULT),
                      help="Path to JSON Schema.")
    lint.add_argument("--format", choices=["text", "json"], default="text")

    args = ap.parse_args()
    if args.cmd != "lint":
        ap.print_help()
        return 2

    schema_path = Path(args.schema)
    if not schema_path.is_file():
        sys.stderr.write("error: schema not found at {}\n".format(schema_path))
        return 2
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)

    paths = collect_paths(args.paths)
    if not paths:
        sys.stderr.write("error: no YAML files found\n")
        return 2

    results = [lint_one(p, schema) for p in paths]

    if args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print("=" * 76)
            print("CARD: {}".format(r["path"]))
            print("STATUS: {}".format(r["summary"]))
            c = r["completeness"]
            print("Completeness: {} / {} ({:.1f}%)".format(c["achieved"], c["total"], c["pct"]))
            if r["schema_errors"]:
                print("\nSchema errors:")
                for e in r["schema_errors"]:
                    print("  - {}".format(e))
            if r["warnings"]:
                print("\nConsistency warnings:")
                for w in r["warnings"]:
                    print("  ! {}".format(w))
            print()
        print("=" * 76)
        print("Linted {} card(s).".format(len(results)))

    return 1 if any(not r["schema_valid"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())

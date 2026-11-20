import json
import os
import re
import sys

STATUS = ["pass", "partial", "fail", "untested"]
EVIDENCE = ["example", "manual", "automated"]
TOP_REQUIRED = ["skill", "version", "evidence_type", "agent", "tested_on", "cases"]
CASE_REQUIRED = ["id", "prompt", "expect", "without_skill", "with_skill"]
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def check_card(path):
    errors = []
    warnings = []
    try:
        with open(path, encoding="utf-8") as f:
            card = json.load(f)
    except ValueError as exc:
        return ["Not valid JSON: %s" % exc], warnings

    if not isinstance(card, dict):
        return ["Top level must be a JSON object"], warnings

    for key in TOP_REQUIRED:
        if key not in card:
            errors.append("Missing field: %s" % key)

    skill = card.get("skill")
    if isinstance(skill, str) and not NAME_RE.match(skill):
        errors.append("skill must be lowercase letters, numbers and hyphens")

    if "evidence_type" in card and card["evidence_type"] not in EVIDENCE:
        errors.append("evidence_type must be one of: %s" % ", ".join(EVIDENCE))

    tested_on = card.get("tested_on")
    if tested_on is not None and not (isinstance(tested_on, str) and DATE_RE.match(tested_on)):
        errors.append("tested_on must look like YYYY-MM-DD")

    cases = card.get("cases")
    if cases is not None:
        if not isinstance(cases, list) or not cases:
            errors.append("cases must be a non-empty list")
            cases = []
        seen = set()
        for i, case in enumerate(cases):
            label = "case %d" % (i + 1)
            if not isinstance(case, dict):
                errors.append("%s must be an object" % label)
                continue
            for key in CASE_REQUIRED:
                if key not in case:
                    errors.append("%s is missing: %s" % (label, key))
            cid = case.get("id")
            if isinstance(cid, str):
                label = "case '%s'" % cid
                if not NAME_RE.match(cid):
                    errors.append("%s: id must be lowercase letters, numbers and hyphens" % label)
                if cid in seen:
                    errors.append("%s: duplicate id" % label)
                seen.add(cid)
            for key in ("without_skill", "with_skill"):
                if key in case and case[key] not in STATUS:
                    errors.append("%s: %s must be one of: %s" % (label, key, ", ".join(STATUS)))
            if case.get("with_skill") == "pass" and case.get("without_skill") == "pass":
                warnings.append("%s: passes without the skill too, so it shows no improvement" % label)

    return errors, warnings


def find_cards(paths):
    found = []
    for p in paths:
        if os.path.isfile(p) and p.endswith(".eval.json"):
            found.append(p)
        elif os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                for name in files:
                    if name.endswith(".eval.json"):
                        found.append(os.path.join(root, name))
    return sorted(found)


def main():
    paths = sys.argv[1:] or ["evals"]
    cards = find_cards(paths)
    if not cards:
        print("ERROR: no .eval.json files found in: %s" % ", ".join(paths))
        sys.exit(1)

    total_errors = 0
    for path in cards:
        errors, warnings = check_card(path)
        print("[%s] %s" % ("FAIL" if errors else "PASS", path))
        for e in errors:
            print("   error:   %s" % e)
        for w in warnings:
            print("   warning: %s" % w)
        total_errors += len(errors)

    print("")
    print("Checked %d eval card(s), %d error(s)" % (len(cards), total_errors))
    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()

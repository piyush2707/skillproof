import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "rules.json"), encoding="utf-8") as f:
    RULES = json.load(f)

NAME_RE = re.compile(RULES["name_pattern"])
LINK_RE = re.compile(r"\]\(([^)\s]+)\)")


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text
    data = {}
    key = None
    for line in lines[1:end]:
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            key = m.group(1)
            val = m.group(2).strip()
            if val in (">", "|", ">-", "|-"):
                val = ""
            data[key] = val
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    for k in data:
        data[k] = data[k].strip().strip('"').strip("'")
    body = "\n".join(lines[end + 1:])
    return data, body


def check_skill(path):
    errors = []
    warnings = []
    with open(path, encoding="utf-8") as f:
        text = f.read()
    folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
    data, body = parse_frontmatter(text)

    if data is None:
        errors.append("Missing frontmatter block (--- ... ---) at top of file")
        return errors, warnings

    name = data.get("name", "")
    if not name:
        errors.append("Missing 'name' in frontmatter")
    else:
        if len(name) > RULES["max_name_length"]:
            errors.append("name is longer than %d characters" % RULES["max_name_length"])
        if not NAME_RE.match(name):
            errors.append("name must be lowercase letters, numbers and hyphens only")
        if name != folder:
            warnings.append("name '%s' does not match folder '%s'" % (name, folder))

    desc = data.get("description", "")
    if not desc:
        errors.append("Missing 'description' in frontmatter")
    else:
        if len(desc) < RULES["min_description_length"]:
            errors.append("description is too short (under %d characters)" % RULES["min_description_length"])
        if len(desc) > RULES["max_description_length"]:
            errors.append("description is longer than %d characters" % RULES["max_description_length"])
        lower = desc.lower()
        if not any(p in lower for p in RULES["trigger_phrases"]):
            warnings.append("description has no clear trigger (e.g. 'Use when ...')")

    body_lines = len(body.splitlines())
    if body_lines > RULES["max_body_lines"]:
        warnings.append("body has %d lines (over %d)" % (body_lines, RULES["max_body_lines"]))

    skill_dir = os.path.dirname(os.path.abspath(path))
    for link in LINK_RE.findall(body):
        if link.startswith(("http://", "https://", "#", "mailto:")):
            continue
        target = link.split("#")[0]
        if target and not os.path.exists(os.path.join(skill_dir, target)):
            errors.append("Broken file reference: %s" % link)

    return errors, warnings


def find_skills(paths):
    found = []
    for p in paths:
        if os.path.isfile(p) and os.path.basename(p) == "SKILL.md":
            found.append(p)
        elif os.path.isdir(p):
            for root, _dirs, files in os.walk(p):
                if "SKILL.md" in files:
                    found.append(os.path.join(root, "SKILL.md"))
    return sorted(found)


def main():
    paths = sys.argv[1:] or ["."]
    skills = find_skills(paths)
    if not skills:
        print("ERROR: no SKILL.md files found in: %s" % ", ".join(paths))
        sys.exit(1)

    total_errors = 0
    for path in skills:
        errors, warnings = check_skill(path)
        status = "FAIL" if errors else "PASS"
        print("[%s] %s" % (status, path))
        for e in errors:
            print("   error:   %s" % e)
        for w in warnings:
            print("   warning: %s" % w)
        total_errors += len(errors)

    print("")
    print("Checked %d skill(s), %d error(s)" % (len(skills), total_errors))
    sys.exit(1 if total_errors else 0)


if __name__ == "__main__":
    main()

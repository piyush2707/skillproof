# Eval Card format

An Eval Card is a file named `<skill>.eval.json` stored in `evals/`.

| Field | Required | Meaning |
|---|---|---|
| skill | yes | Skill name (lowercase letters, numbers, hyphens) |
| version | yes | Version of the skill that was tested |
| evidence_type | yes | `example`, `manual` or `automated` |
| agent | yes | Agent and model the cases were run on |
| tested_on | yes | Date, `YYYY-MM-DD` |
| cases | yes | List of test cases (at least one) |

Each case:

| Field | Required | Meaning |
|---|---|---|
| id | yes | Unique, lowercase with hyphens |
| prompt | yes | What the user asked |
| expect | yes | What a good answer must contain |
| without_skill | yes | Result without the skill |
| with_skill | yes | Result with the skill |
| notes | no | Anything worth knowing |

Result values: `pass`, `partial`, `fail`, `untested`.

Use `example` only for sample data. Use `manual` when a person ran the cases
and recorded the results honestly.

# SkillProof

**Test, score and showcase AI agent skills and prompts. Free, open source, runs in your browser.**

Agent skills are easy to write and hard to trust. SkillProof checks whether a
skill is well-formed, how much context it costs, whether it clashes with other
skills, and whether it has real evidence that it works.

> Status: early development (v0.1 in progress). Features below are marked
> as planned until they ship and are tested.

## Modules

| Module | What it does | Status |
|---|---|---|
| Validator Action | Checks SKILL.md structure and quality on every pull request | Planned |
| Context Meter | Estimates how much context your skills use before any task starts | Planned |
| Conflict Map | Flags skills whose descriptions overlap and may confuse an agent | Planned |
| Eval Cards | JSON test cases with before/after evidence | Planned |
| Skill Pages | Auto-generated demo page for every skill | Planned |
| Flagship skills | RAG Failure Attribution, RepoReel | Planned |

## Why SkillProof

- Most skill repos are collections of instructions with no proof.
- SkillProof adds measurable checks and visible evidence.
- Everything runs on GitHub (Actions and Pages), with no servers or paid APIs.

## Compatibility

SkillProof reads the `SKILL.md` format (name and description in frontmatter).
Compatibility with specific agents will be listed here only after testing.

## Contributing

See `CONTRIBUTING.md` (coming soon). New skills and checks are welcome.

## License

MIT. See `LICENSE`.

Made by [Piyush](https://github.com/piyush2707)

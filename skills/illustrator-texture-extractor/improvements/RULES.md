# Illustrator Texture Extractor Improvement Queue Rules

This directory is a review queue for reusable experience discovered during real Illustrator extraction work. Each Markdown file under `pending/` is one candidate, not an established Skill rule. A maintainer must review it before moving anything into `SKILL.md`, a reference, or a script.

## Recording workflow

- Record only behavior observed in a real run with concrete evidence such as a COM error, Illustrator warning, object inventory, export measurement, alpha report, or visual artifact.
- Record only after the user's primary task is safe and verified. Logging must not interrupt recovery or delay delivery.
- Do not list, search, or read existing files under `pending/` before recording. Duplicate detection belongs to maintainer review.
- Create exactly one new Markdown file per candidate. Do not append to or rewrite an existing entry.
- Name new files `YYYY-MM-DDTHH-mm-ss-short-title.md`. Use a concise lowercase ASCII slug and add a numeric suffix only if that exact path already exists.
- Set `Status` to `pending review`.
- Remove user secrets, private document contents, customer names, product-specific coordinates, object indices, and unnecessary machine paths.
- Do not promote a candidate into established guidance or code without explicit maintainer review.

## Entry template

```markdown
# Short title

- Status: pending review
- Date: YYYY-MM-DD
- Context: What Illustrator operation and environment exposed the behavior.
- Observation: Exact behavior, error, warning, or result.
- Evidence: Relevant command, inventory fact, export report, or visual artifact.
- Workaround: What safely unblocked or improved the task.
- Candidate destination: Possible `SKILL.md`, workflow, or script location.
- Review notes: Leave blank for the maintainer.
```

## Maintainer review

Only when review or absorption is explicitly requested, read the files under `pending/`, consolidate duplicates, and validate the evidence. Promote accepted knowledge to the smallest appropriate canonical destination, then remove the reviewed pending files. Do not treat an unreviewed entry as established guidance.

---
id: META-NAMING-001
type: specification
title: Vault Naming Conventions & Taxonomy Rules
status: evergreen
tags:
  - meta
  - naming
  - conventions
---

# Vault Naming Conventions & Taxonomy Rules

To maintain high searchability, human readability, and smooth automated tooling, notes and folders follow these standard conventions.

---

## 1. Directory Structure Conventions

Top-level directories use a two-digit decimal prefix indicating their lifecycle role:
- `00-inbox/`: Temporary intake, fleeting captures, unorganized thoughts.
- `01-daily/`: Timestamped daily journals and logs (`YYYY-MM-DD.md`).
- `10-projects/`: Finite initiatives with defined completion states.
- `20-areas/`: Ongoing spheres of activity and standards without end dates.
- `30-knowledge/`: Evergreen atomic concepts, frameworks, and reference guides.
- `40-decisions/`: Architecture & Strategy Decision Records (ADRs).
- `50-playbooks/`: Verified repeatable standard operating procedures (SOPs).
- `60-personal/`: Private life administration, goals, and personal infrastructure.
- `90-archives/`: Inactive, completed, or deprecated material retained for history.

---

## 2. File Naming Rules

### A. General Markdown Notes
- Use **kebab-case** (lowercase with hyphens) for all general notes, playbooks, and decisions:
  - `git-workflow-conventions.md`
  - `visual-slam-survey.md`
  - `use-postgresql-for-storage.md`
- Avoid spaces, special symbols (`!`, `@`, `#`, `$`, `%`, `^`, `&`, `*`), and trailing punctuation in filenames.

### B. Daily Notes
- Always name daily notes using strict ISO-8601 calendar date format:
  - `YYYY-MM-DD.md` (e.g., `2026-09-20.md`).

### C. Prefixed Content Types
When multiple notes share a topic, prefixing can enhance sortability:
- Concept notes: `concept-<slug>.md`
- Experiment logs: `experiment-<slug>.md`
- Literature reviews: `literature-<slug>.md`
- Project charters: `project-<slug>.md`
- Decisions: `decision-<slug>.md` or `ADR-YYYY-<number>-<slug>.md`

---

## 3. Wikilink Guidelines
- Use double-bracket wikilinks targeting the base filename: `[[concept-pid-controller]]` or piped links `[[concept-pid-controller|PID Controller]]`.
- Always verify that links inside documentation and playbooks point to valid existing files.

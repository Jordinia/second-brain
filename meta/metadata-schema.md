---
id: META-SCHEMA-001
type: specification
title: Metadata Schema & Frontmatter Specification
status: evergreen
tags:
  - meta
  - schema
  - yaml
---

# Metadata Schema & Frontmatter Specification

This document defines the canonical YAML frontmatter schemas, allowed field enums, and identifier patterns required across all notes in the vault.

---

## 1. Universal Base Schema

Every note in the vault must contain at minimum:

```yaml
---
id: <PREFIX>-<TIMESTAMP>
type: <note-type>
title: <human-readable title>
date: YYYY-MM-DD
tags:
  - <primary-tag>
---
```

---

## 2. Type-Specific Prefix Registry

To prevent ID collisions when multiple notes are generated in a single day, all notes follow this registry:

| Note Type | Prefix Pattern | Format | Example |
| :--- | :--- | :--- | :--- |
| **Daily Note** | `DAILY-` | `DAILY-{{date:YYYYMMDD}}` | `DAILY-20260920` |
| **Quick Capture** | `CAP-` | `CAP-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `CAP-20260920-143022` |
| **Project** | `PRJ-` | `PRJ-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `PRJ-20260920-143022` |
| **Area** | `AREA-` | `AREA-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `AREA-20260920-143022` |
| **Meeting** | `MTG-` | `MTG-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `MTG-20260920-143022` |
| **Experiment** | `EXP-` | `EXP-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `EXP-20260920-143022` |
| **Learning Note** | `LRN-` | `LRN-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `LRN-20260920-143022` |
| **Literature Note** | `LIT-` | `LIT-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `LIT-20260920-143022` |
| **Concept Note** | `KB-` | `KB-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `KB-20260920-143022` |
| **Decision (ADR)** | `ADR-` | `ADR-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `ADR-20260920-143022` |
| **Playbook (SOP)** | `PB-` | `PB-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `PB-20260920-143022` |

> [!NOTE] Programmatic Agent Note Generation
> Automated agents (Hermes, Antigravity, Codex) creating notes programmatically MUST verify uniqueness prior to writing, and may optionally utilize UUIDv4 or ULID strings in the ID suffix.

---

## 3. Allowed Enumerations

### Note Status (`status`)
- **Projects**: `planned`, `active`, `paused`, `completed`, `cancelled`
- **Areas**: `active`, `maintenance`, `inactive`
- **Concepts**: `draft`, `provisional`, `evergreen`, `superseded`
- **Decisions**: `proposed`, `accepted`, `deprecated`, `superseded`
- **Playbooks**: `draft`, `active`, `deprecated`
- **Experiments**: `planned`, `running`, `completed`, `failed`
- **Captures**: `inbox`, `processed`, `discarded`

### Concept Confidence (`confidence`)
- `raw`: Fleeting thought or early note; unverified.
- `provisional`: Supported by initial references or testing.
- `tested`: Confirmed through practical implementation or lab work.
- `verified`: Thoroughly proven concept with repeatable evidence.

### Literature Reading Status (`reading_status`)
- `unread`: Captured or queued paper.
- `in-progress`: Actively being read and annotated.
- `read`: Fully digested with key contributions extracted.
- `reference`: Kept for citation or background reference.

---

## 4. Retrieval-Augmented Generation Flag (`rag_include`)
Notes intended for automated agent ingestion and RAG search indexing should explicitly include:
```yaml
rag_include: true
```
Ephemeral daily scratchpads, temporary meeting stubs, or raw inbox dumps may omit this flag or set it to `false`.

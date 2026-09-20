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
id: <PREFIX>-<IDENTIFIER>
type: <note-type>
tags:
  - <primary-tag>
---
```

---

## 2. Type-Specific Requirements & Prefix Registry

Rather than forcing every note into one artificial shape, note types define their own semantic required fields while strictly conforming to the prefix registry:

| Note Type | Prefix | Format Pattern | Required Fields | Example ID |
| :--- | :--- | :--- | :--- | :--- |
| **`daily`** | `DAILY-` | `DAILY-{{date:YYYYMMDD}}` | `id`, `type`, `date`, `status`, `tags` | `DAILY-20260920` |
| **`capture`** | `CAP-` | `CAP-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `status`, `created_at`, `tags` | `CAP-20260920-143022` |
| **`project`** | `PRJ-` | `PRJ-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `status`, `tags` | `PRJ-20260920-143022` |
| **`area`** | `AREA-` | `AREA-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `status`, `tags` | `AREA-20260920-143022` |
| **`concept`** | `KB-` | `KB-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `status`, `tags` | `KB-20260920-143022` |
| **`decision`** | `ADR-` | `ADR-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `status`, `date`, `tags` | `ADR-20260920-143022` |
| **`experiment`** | `EXP-` | `EXP-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `status`, `date`, `tags` | `EXP-20260920-143022` |
| **`learning-note`** | `LRN-` | `LRN-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `date`, `tags` | `LRN-20260920-143022` |
| **`literature`** | `LIT-` | `LIT-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `year`, `reading_status`, `tags` | `LIT-20260920-143022` |
| **`meeting`** | `MTG-` | `MTG-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `date`, `tags` | `MTG-20260920-143022` |
| **`playbook`** | `PB-` | `PB-{{date:YYYYMMDD}}-{{time:HHmmss}}` | `id`, `type`, `title`, `status`, `date`, `tags` | `PB-20260920-143022` |
| **`specification`**| `META-` | `META-<NAME>-<NNN>` | `id`, `type`, `title`, `status`, `tags` | `META-SCHEMA-001` |
| **`profile`** | `META-` | `META-PROFILE-<SUFFIX>` | `id`, `type`, `title`, `tags` | `META-PROFILE-EXAMPLE` |

> [!NOTE] Framework Documents & Programmatic Agent Note Generation
> - **Framework Governance**: Governance specifications and profile definitions reside in the reserved `META-` prefix namespace.
> - **Automated Agents**: Agents (Hermes, Antigravity, Codex) creating notes programmatically MUST verify ID uniqueness prior to writing, and may optionally utilize UUIDv4 or ULID strings in the ID suffix for collision resistance.

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

---
id: META-VAULT-CONTRACT-001
type: specification
title: The Second Brain Vault Contract & Core Invariants
status: evergreen
tags:
  - meta
  - specification
  - governance
---

# The Second Brain Vault Contract & Core Invariants

This document establishes the ten constitutional invariants of this knowledge repository. Any tool, automated agent, or workflow operating within this vault must conform to these principles.

---

### Invariant 1: Local-First Plaintext Source of Truth
The Markdown files on disk are the durable canonical memory. External databases, vector embeddings, cloud indexes, and agent conversation logs are transient views, not primary storage. If an insight or record is generated, it must be persisted as Markdown with standard YAML frontmatter.

### Invariant 2: Git-Native Version Control
All modifications are tracked through Git. For regular knowledge work, `main` functions as a living trunk. High-friction feature branches are reserved for large structural reorganizations, taxonomy shifts, or automated bulk migrations. Commits should be atomic and follow conventional commit syntax.

### Invariant 3: Obsidian Core Compatibility (Zero Plugin Lock-in)
The baseline vault functions 100% using official **Obsidian Core** features, native YAML properties, and Markdown syntax. No community plugins (such as Dataview or Templater) are required for baseline functionality or note creation.

### Invariant 4: Structured Numeric PKM Taxonomy
Notes are organized across a predictable 9-folder lifecycle hierarchy (`00-inbox` through `90-archives`). User knowledge notes should not be stored at the vault root. Reserved framework governance documents (e.g. `README.md`, `AGENTS.md`, `LICENSE`, `VAULT-STRUCTURE.md`) are explicit exceptions. Notes progress naturally from capture to active projects, evergreen knowledge, and eventual archive.

### Invariant 5: Type-Specific Prefix Registry
User-content note types use the timestamped prefix registry (`DAILY-`, `CAP-`, `PRJ-`, `AREA-`, `MTG-`, `EXP-`, `LRN-`, `LIT-`, `KB-`, `ADR-`, `PB-`) to guarantee collision resistance across multiple notes created on the same day. Framework governance documents use the reserved `META-` namespace.

### Invariant 6: Recoverable & Targeted Agent Mutations
AI assistants (Hermes, Antigravity, Claude, Codex) operate under strict safety guardrails:
1. Always preserve pre-mutation recoverable copies before overwriting existing documents.
2. Make surgical, targeted edits rather than rewriting intact files.
3. Never execute unrecoverable deletions (move to `.trash/` instead).
4. Always cite source note titles and IDs when synthesizing knowledge.

### Invariant 7: Resilient Internal Wikilinking
Notes connect using double-bracket wikilinks (`[[Target Note]]`). Internal links should reflect semantic associations. While documentation notes require valid targets, Obsidian's paradigm of intentional stub creation (`[[Future Thought]]`) in ordinary notes is embraced.

### Invariant 8: Strict Binary & Asset Separation
Git tracks knowledge, code configs, and lightweight attachments (<10MB). Bulky binaries, large video recordings, heavy datasets, and model weights must remain outside the Git tree.

### Invariant 9: Privacy by Default
The framework template contains zero personal identifiers, credentials, or proprietary data. When initializing a personal instance from this template, the repository should be initialized as **Private** to safeguard personal thoughts, finances, and journal entries.

### Invariant 10: Human Sovereignty & Derivation
The vault serves human cognitive clarity. Automated agents assist, summarize, draft, and organize, but the human user retains executive authority over taxonomy evolution, project priorities, and final archiving.

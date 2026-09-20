# AI Agent Policy & Knowledge Vault Protocol

This document establishes the universal rules of engagement for AI assistants (Hermes Agent, Antigravity, Claude Code, Codex, and local LLMs) operating within this knowledge repository.

---

## 1. Source of Truth & Durability
1. **Markdown Vault as Primary Memory**: The local Markdown files in this vault represent the canonical source of truth. Model context windows, conversation histories, and vector database embeddings are transient projections.
2. **Durable Persistence**: When an agent synthesizes a key decision, technical insight, architecture plan, or research review, it must be persisted as a Markdown note with proper frontmatter schema conforming to `meta/metadata-schema.md`.
3. **Local Profile Context**: If `meta/profile.md` exists, consult it for user preferences and identity. Do not commit private details from `profile.md` to public branches.

---

## 2. Permissive Safety & Mutation Rules
1. **Pre-Write State Preservation**: Agents must create a recoverable backup of any existing file before executing an update, overwrite, or structural refactor.
2. **Surgical, Targeted Edits**: Prefer modifying specific sections, appending entries, or editing discrete YAML frontmatter fields rather than rewriting intact files.
3. **Soft Deletion Only**: Never execute unrecoverable deletions (`rm`). Move obsolete or deleted files into `.trash/`.
4. **Preserve Raw Captures**: Never modify or delete unprocessed quick captures or raw notes in `00-inbox/`. Always process them by creating new curated notes and moving the capture to processed status.
5. **Citations in Responses**: When answering questions using vault knowledge, always cite the note title, ID, and relative vault path.

---

## 3. Vault Organization & Routing
- **`00-inbox/`**: Destination for quick captures, voice transcripts, and AI drafts.
- **`01-daily/`**: Chronological daily tracking (`YYYY-MM-DD.md`).
- **`10-projects/`**: Active outcomes with concrete completion criteria.
- **`20-areas/`**: Long-term domains of responsibility without target dates.
- **`30-knowledge/`**: Evergreen concept notes, mathematical derivations, technical guides.
- **`40-decisions/`**: Architecture and strategy decision records (ADRs).
- **`50-playbooks/`**: Verified, repeatable standard operating procedures (SOPs).
- **`60-personal/`**: Personal infrastructure, health, finance, and life admin.
- **`90-archives/`**: Completed projects, superseded knowledge, and inactive material.

---

## 4. Git & Version Control Behavior
1. **Trunk Discipline**: Normal note creation and editing is committed to `main`.
2. **Conventional Syntax**: Commit messages must follow conventional commit taxonomy:
   ```text
   type(scope): description
   ```
   (e.g., `note(controls): explain state feedback`, `daily: update priorities`, `chore(meta): refine schema`).
3. **Safety Restrictions**:
   - Never force-push (`git push --force`) to any branch.
   - Never commit environment files (`.env*`), private keys, or API tokens.
   - Do not silently resolve merge conflicts without verifying note content integrity.

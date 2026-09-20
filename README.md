# 🧠 Second Brain: Open-Source Obsidian Knowledge Framework

> A local-first, Git-native, zero-plugin personal knowledge vault and GitHub Template Repository. Designed for deep engineering, research, and seamless AI agent collaboration.

---

## 🔒 Critical Privacy Notice: How to Use This Template

> [!WARNING] Keep Your Personal Second Brain Private
> This repository (`Jordinia/second-brain`) is a **public open-source template**.
> 
> When creating your personal second brain, **do NOT clone this repository directly** if you intend to write personal journals, confidential projects, or life admin notes. If you clone it directly, you cannot push private notes back to this public repository.
> 
> **The Proper Onboarding Flow**:
> 1. Click the green **"Use this template"** button at the top of this GitHub repository $\rightarrow$ select **"Create a new repository"**.
> 2. Name your repository (e.g., `my-second-brain` or `vault`) and **select "Private"**.
> 3. Clone *your newly created private repository* to your local machine:
>    ```bash
>    git clone git@github.com:<your-username>/<your-private-vault>.git
>    ```
> 4. Open Obsidian $\rightarrow$ click **"Open folder as vault"** $\rightarrow$ select your cloned folder.

---

## ⚡ 5-Minute Quick Start

1. **Launch Obsidian**: Open the repository folder as a vault.
2. **Open Today's Daily Note**:
   - Press `Ctrl + P` (or `Cmd + P` on macOS) $\rightarrow$ type `Daily notes: Open today's daily note` $\rightarrow$ press `Enter`.
   - Your daily log is created under `01-daily/YYYY-MM-DD.md` pre-populated with today's priorities, meals, and tasks.
3. **Capture a Fleeting Thought**:
   - Create a note in `00-inbox/quick-capture/` using the template at `templates/quick-capture.md`.
4. **Create Your First Concept Note**:
   - Create a note in `30-knowledge/` using `templates/concept.md`. Link it from other notes using `[[concept-name]]`.
5. **Sync Your Changes**:
   - In your terminal:
     ```bash
     git add -A
     git commit -m "daily: initialize first notes"
     git push origin main
     ```

---

## 🏛️ Vault Architecture & Taxonomy

Notes follow a structured numeric lifecycle (`00` to `90`) inspired by the PARA method:

```text
second-brain/
├── 00-inbox/          # Raw captures, voice notes, and AI drafts awaiting triage
├── 01-daily/          # Chronological daily journals and habit logs (YYYY-MM-DD.md)
├── 10-projects/       # Active initiatives with defined completion states
├── 20-areas/          # Long-term domains of responsibility (career, health, finance)
├── 30-knowledge/      # Evergreen atomic concepts, literature reviews, and formulas
├── 40-decisions/      # Architecture & Strategy Decision Records (ADRs)
├── 50-playbooks/      # Verified, repeatable Standard Operating Procedures (SOPs)
├── 60-personal/       # Private life admin, goals, and personal infrastructure
├── 90-archives/       # Inactive, completed, or deprecated notes retained for history
├── assets/            # Lightweight diagrams and attachments (<10MB)
├── templates/         # 11 Core-Obsidian compatible Markdown templates
├── examples/          # 6 realistic sample notes demonstrating links and frontmatter
├── meta/              # Metadata schema, prefix registry, and naming conventions
├── scripts/           # Standalone vault linter and schema validation tooling
└── integrations/      # Documentation for GitSync, local LLMs, and AI agents
```

---

## 🎯 Core Features & Invariants

- **Zero Plugin Lock-in**: 100% compliant with **Obsidian Core**. No Dataview or Templater plugins required for baseline operation.
- **Collision-Resistant Note IDs**: Formal Type-Specific Prefix Registry (`DAILY-`, `CAP-`, `PRJ-`, `AREA-`, `MTG-`, `EXP-`, `LRN-`, `LIT-`, `KB-`, `ADR-`, `PB-`).
- **AI Agent Protocol Ready**: Pre-configured with [`AGENTS.md`](AGENTS.md), establishing strict safety invariants (recoverable pre-write state preservation, surgical edits, and source attribution) for tools like Hermes Agent, Antigravity, Claude Code, and Codex.
- **Link Auto-Update**: Configured out of the box with `"alwaysUpdateLinks": true` in `.obsidian/app.json` to prevent broken wikilinks when notes are renamed.
- **Automated CI Validation**: Shipped with [`scripts/validate_vault.py`](scripts/validate_vault.py) and GitHub Actions to verify YAML schemas, template placeholders, and secret leaks via Gitleaks.

---

## 🤝 Contributing

Contributions of universal templates, playbooks, or script improvements are welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for details.

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

Authored by **Rizki Awanta Jordhie** ([@Jordinia](https://github.com/Jordinia)).

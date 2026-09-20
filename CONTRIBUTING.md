# Contributing to Second Brain

Thank you for your interest in improving the **Second Brain** open-source knowledge framework!

---

## 🏛️ Guiding Principles

1. **Obsidian Core Only**: All contributions must function entirely within official Obsidian Core without requiring community plugins (e.g. Dataview or Templater).
2. **Zero Leakage / No Personal Data**: Templates, playbooks, and documentation must never contain real personal email addresses, private IP addresses, credentials, or proprietary material.
3. **Collision-Resistant IDs**: New templates must follow the Type-Specific Prefix Registry documented in `meta/metadata-schema.md`.
4. **Valid Wikilinks**: Any markdown links added to documentation or playbooks must resolve to existing files.

---

## 🛠️ How to Contribute

1. **Fork and Clone**:
   ```bash
   git clone https://github.com/<your-username>/second-brain.git
   cd second-brain
   ```
2. **Create a Feature Branch**:
   ```bash
   git checkout -b feat/add-new-template
   ```
3. **Install Dev Tooling & Validate Locally**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements-dev.txt
   python scripts/validate_vault.py .
   ```
4. **Commit with Conventional Syntax**:
   ```bash
   git commit -m "feat(templates): add system-architecture template"
   ```
5. **Open a Pull Request**: Submit your PR targeting `main`. Ensure all automated CI checks (schema validation and Gitleaks secret detection) pass.

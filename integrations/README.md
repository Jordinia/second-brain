# integrations: Advanced Automation & Agent Tooling

> [!NOTE] Decoupled Architecture
> The core second brain functions 100% without any external tools, Python scripts, or Docker containers. This directory provides documentation and architectural patterns for optional power-user integrations.

---

## 1. Multi-Device Mobile Sync (GitSync)

To synchronize your vault between desktop and mobile devices (Android / iOS) without proprietary cloud sync:
1. **Tool**: Use **GitSync** (Android) or **Working Copy** (iOS).
2. **Protocol**: Follow the "Pull on Launch, Push on Exit" workflow documented in [`50-playbooks/git-workflow-conventions.md`](../50-playbooks/git-workflow-conventions.md).
3. **Automated Desktop Sync**: On Linux/macOS desktops, a lightweight systemd timer or cron job can execute `git pull` and `git push` periodically.

---

## 2. AI Assistant Integration (Hermes / Claude / Codex)

This vault is engineered to be AI-agent native:
- **`AGENTS.md`**: Provides the top-level rules of engagement for coding assistants.
- **`meta/profile.md`**: (Copied from `meta/profile.example.md`) provides local context on your goals, active projects, and preferred coding style without committing personal data to remote repos.
- **Tooling Protocols**:
  - Pre-write state preservation: Agents must backup notes before destructive edits.
  - Soft deletions: Obsolete files are moved to `.trash/`.

---

## 3. Model Context Protocol (MCP)

For clients that support the Model Context Protocol (e.g., Claude Desktop, Antigravity, or Cursor), you can connect a local filesystem or Obsidian MCP server pointing to the vault directory to enable real-time reading, semantic search, and append operations directly from chat interfaces.

#!/usr/bin/env python3
"""
scripts/validate_vault.py
Three-tier validator for Second Brain Obsidian knowledge vault.

Validates:
1. Frontmatter YAML parsing and schema conformance (id, type, tags).
2. Template variable compliance (strictly Obsidian Core templates syntax).
3. Three-tier wikilink integrity:
   - ERROR: Malformed syntax, path traversal escaping vault, or broken links
     inside framework docs (README, VAULT-STRUCTURE, meta/, 50-playbooks/, examples/).
   - WARNING: Unresolved links in ordinary user notes (allowed PKM stubs).
   - IGNORE: Placeholder links in templates/ (e.g., [[<topic>]]).
"""

import sys
import os
import re
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install -r requirements-dev.txt", file=sys.stderr)
    sys.exit(1)

ALLOWED_CORE_VARS = {
    "title",
    "date",
    "time",
}

ALLOWED_MOMENT_FORMATS = re.compile(r"^(date|time):[A-Za-z0-9_\-:]+$")

# Framework docs where broken links are treated as errors
FRAMEWORK_DOC_DIRS = {"meta", "50-playbooks", "examples"}
FRAMEWORK_DOC_FILES = {"README.md", "VAULT-STRUCTURE.md", "CONTRIBUTING.md", "AGENTS.md"}

# Note types allowed in metadata schema
VALID_NOTE_TYPES = {
    "daily",
    "capture",
    "project",
    "area",
    "meeting",
    "experiment",
    "learning-note",
    "literature",
    "concept",
    "decision",
    "playbook",
    "specification",
    "profile",
}

TYPE_PREFIX_MAP = {
    "daily": "DAILY-",
    "capture": "CAP-",
    "project": "PRJ-",
    "area": "AREA-",
    "meeting": "MTG-",
    "experiment": "EXP-",
    "learning-note": "LRN-",
    "literature": "LIT-",
    "concept": "KB-",
    "decision": "ADR-",
    "playbook": "PB-",
    "specification": "META-",
    "profile": "META-",
}

TYPE_REQUIRED_FIELDS = {
    "daily": ["date", "status"],
    "capture": ["status", "created_at"],
    "project": ["title", "status"],
    "area": ["title", "status"],
    "concept": ["title", "status"],
    "decision": ["title", "status", "date"],
    "experiment": ["title", "status", "date"],
    "learning-note": ["title", "date"],
    "literature": ["title", "year", "reading_status"],
    "meeting": ["title", "date"],
    "playbook": ["title", "status", "date"],
    "specification": ["title", "status"],
    "profile": ["title"],
}

ALLOWED_STATUS = {
    "project": {"planned", "active", "paused", "completed", "cancelled"},
    "area": {"active", "maintenance", "inactive"},
    "concept": {"draft", "provisional", "evergreen", "superseded"},
    "decision": {"proposed", "accepted", "deprecated", "superseded"},
    "playbook": {"draft", "active", "deprecated"},
    "experiment": {"planned", "running", "completed", "failed"},
    "capture": {"inbox", "processed", "discarded"},
    "daily": {"active", "archived"},
    "specification": {"draft", "active", "evergreen", "deprecated"},
}

ALLOWED_READING_STATUS = {"unread", "in-progress", "read", "reference"}
ALLOWED_CONFIDENCE = {"raw", "provisional", "tested", "verified"}

def extract_frontmatter(content: str):
    """Extract raw YAML frontmatter from markdown content if present."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1]
    return None

def validate_templates(vault_dir: Path):
    """Validate that all templates only use permitted Obsidian Core placeholders."""
    errors = []
    templates_dir = vault_dir / "templates"
    if not templates_dir.exists():
        return errors

    var_pattern = re.compile(r"\{\{([^}]+)\}\}")

    for file_path in templates_dir.glob("*.md"):
        content = file_path.read_text(encoding="utf-8")
        matches = var_pattern.findall(content)
        for var in matches:
            var_clean = var.strip()
            if var_clean in ALLOWED_CORE_VARS:
                continue
            if ALLOWED_MOMENT_FORMATS.match(var_clean):
                continue
            errors.append(
                f"[Template Syntax Error] {file_path.relative_to(vault_dir)}: "
                f"Unsupported template variable '{{{{{var}}}}}'. Only Obsidian Core variables and Moment formatters are permitted."
            )
    return errors

def validate_frontmatter(vault_dir: Path):
    """Validate YAML frontmatter across all markdown files (excluding templates)."""
    errors = []
    seen_ids = {}
    
    for file_path in sorted(vault_dir.rglob("*.md")):
        rel_path = file_path.relative_to(vault_dir)
        
        # Skip templates folder and dot-directories
        if str(rel_path).startswith("templates/") or any(part.startswith(".") for part in rel_path.parts):
            continue

        content = file_path.read_text(encoding="utf-8")
        raw_fm = extract_frontmatter(content)
        
        if raw_fm is None:
            # Informational READMEs without frontmatter are permitted
            if file_path.name == "README.md" or file_path.name in ("CONTRIBUTING.md", "AGENTS.md", "LICENSE"):
                continue
            errors.append(f"[Missing Frontmatter] {rel_path}: Note lacks valid YAML frontmatter delimiters ('---').")
            continue

        try:
            data = yaml.safe_load(raw_fm)
        except yaml.YAMLError as exc:
            errors.append(f"[YAML Syntax Error] {rel_path}: Failed to parse YAML frontmatter: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"[Malformed Frontmatter] {rel_path}: Frontmatter is not a key-value mapping.")
            continue

        # 1. Base required fields check for all notes (id, type, tags)
        if "id" not in data or not data["id"]:
            errors.append(f"[Missing ID] {rel_path}: Missing required 'id' frontmatter field.")
            continue
        
        note_id = str(data["id"]).strip()

        # Check ID uniqueness across entire vault
        if note_id in seen_ids:
            errors.append(f"[Duplicate ID] {rel_path}: ID '{note_id}' is already used by '{seen_ids[note_id]}'.")
        else:
            seen_ids[note_id] = rel_path

        if "type" not in data or not data["type"]:
            errors.append(f"[Missing Type] {rel_path}: Missing required 'type' frontmatter field.")
            continue

        note_type = str(data["type"]).strip()
        if note_type not in VALID_NOTE_TYPES:
            errors.append(f"[Invalid Type] {rel_path}: Unknown note type '{note_type}'.")
            continue

        if "tags" not in data or data["tags"] is None:
            errors.append(f"[Missing Tags] {rel_path}: Missing required 'tags' frontmatter field.")
        elif not isinstance(data["tags"], list):
            errors.append(f"[Malformed Tags] {rel_path}: 'tags' must be a YAML list.")

        # 2. Check Type-Specific ID Prefix
        expected_prefix = TYPE_PREFIX_MAP.get(note_type)
        if expected_prefix and not note_id.startswith(expected_prefix):
            errors.append(
                f"[Prefix Mismatch] {rel_path}: Note type '{note_type}' requires ID prefix '{expected_prefix}', got '{note_id}'."
            )

        # 3. Check Type-Specific Required Fields
        req_fields = TYPE_REQUIRED_FIELDS.get(note_type, [])
        for field in req_fields:
            if field not in data or data[field] is None or data[field] == "":
                errors.append(f"[Missing Field] {rel_path}: Note type '{note_type}' requires '{field}' frontmatter field.")

        # 4. Check Allowed Enums
        if note_type in ALLOWED_STATUS and "status" in data and data["status"]:
            if str(data["status"]).strip() not in ALLOWED_STATUS[note_type]:
                errors.append(
                    f"[Invalid Status] {rel_path}: Status '{data['status']}' is invalid for type '{note_type}'. "
                    f"Allowed: {sorted(ALLOWED_STATUS[note_type])}"
                )

        if "reading_status" in data and data["reading_status"]:
            if str(data["reading_status"]).strip() not in ALLOWED_READING_STATUS:
                errors.append(
                    f"[Invalid Reading Status] {rel_path}: Reading status '{data['reading_status']}' is invalid. "
                    f"Allowed: {sorted(ALLOWED_READING_STATUS)}"
                )

        if "confidence" in data and data["confidence"]:
            if str(data["confidence"]).strip() not in ALLOWED_CONFIDENCE:
                errors.append(
                    f"[Invalid Confidence] {rel_path}: Confidence '{data['confidence']}' is invalid. "
                    f"Allowed: {sorted(ALLOWED_CONFIDENCE)}"
                )

    return errors

def validate_wikilinks(vault_dir: Path):
    """Perform three-tier wikilink verification."""
    errors = []
    warnings = []

    # Map existing files by filename stem (for [[note-name]]) and relative path
    existing_stems = {}
    for f in vault_dir.rglob("*.md"):
        if any(part.startswith(".") for part in f.parts):
            continue
        existing_stems[f.stem] = f
        existing_stems[str(f.relative_to(vault_dir))] = f
        existing_stems[str(f.relative_to(vault_dir)).replace(".md", "")] = f

    wikilink_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    for file_path in vault_dir.rglob("*.md"):
        rel_path = file_path.relative_to(vault_dir)
        if any(part.startswith(".") for part in rel_path.parts):
            continue

        # Ignore templates/ for broken link checks
        if str(rel_path).startswith("templates/"):
            continue

        is_framework_doc = (
            file_path.name in FRAMEWORK_DOC_FILES or 
            any(part in FRAMEWORK_DOC_DIRS for part in rel_path.parts)
        )

        content = file_path.read_text(encoding="utf-8")
        # Strip fenced code blocks and inline code spans so illustrative examples aren't treated as links
        cleaned_content = re.sub(r"```[\s\S]*?```", "", content)
        cleaned_content = re.sub(r"`[^`\n]+`", "", cleaned_content)

        matches = wikilink_pattern.findall(cleaned_content)

        for raw_link in matches:
            # Handle piped wikilinks [[target|display text]]
            target = raw_link.split("|")[0].strip()
            # Remove header anchors [[target#section]]
            target = target.split("#")[0].strip()

            if not target:
                continue

            # Check for path traversal escaping vault
            if ".." in target:
                errors.append(f"[Security Error] {rel_path}: Link '{raw_link}' attempts path traversal.")
                continue

            # Strip .md suffix if present
            target_clean = target[:-3] if target.endswith(".md") else target

            # Check if target exists in vault
            exists = (
                target_clean in existing_stems or
                target in existing_stems or
                (vault_dir / f"{target_clean}.md").exists()
            )

            if not exists:
                msg = f"{rel_path}: Unresolved wikilink target '[[{target}]]'"
                if is_framework_doc:
                    errors.append(f"[Broken Framework Link] {msg}")
                else:
                    warnings.append(f"[Unresolved Stub] {msg}")

    return errors, warnings

def main():
    target_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()
    print(f"=== Validating Obsidian Vault at: {target_dir} ===")

    all_errors = []
    
    # 1. Template validation
    print("[1/3] Validating template variables...")
    template_errors = validate_templates(target_dir)
    all_errors.extend(template_errors)

    # 2. Frontmatter schema validation
    print("[2/3] Validating frontmatter schemas...")
    fm_errors = validate_frontmatter(target_dir)
    all_errors.extend(fm_errors)

    # 3. Three-tier wikilink validation
    print("[3/3] Validating wikilink integrity...")
    link_errors, link_warnings = validate_wikilinks(target_dir)
    all_errors.extend(link_errors)

    print("\n--- Summary ---")
    if link_warnings:
        print(f"Warnings ({len(link_warnings)}):")
        for w in link_warnings:
            print(f"  {w}")

    if all_errors:
        print(f"\nFAILED: Found {len(all_errors)} error(s):", file=sys.stderr)
        for err in all_errors:
            print(f"  ❌ {err}", file=sys.stderr)
        sys.exit(1)
    else:
        print("✅ PASSED: Vault passed all validation checks successfully!")
        sys.exit(0)

if __name__ == "__main__":
    main()

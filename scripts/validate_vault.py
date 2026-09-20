#!/usr/bin/env python3
"""
scripts/validate_vault.py
Three-tier validator for Second Brain Obsidian knowledge vault.

Validates:
1. Template variable compliance and rendered template frontmatter schema.
2. Frontmatter YAML parsing, schema conformance, ID prefix/pattern matching,
   enum constraints, and duplicate ID detection across all notes.
3. Three-tier wikilink integrity with cross-platform path normalization and
   safe asset / embed resolution.
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
FRAMEWORK_DOC_FILES = {"README.md", "VAULT-STRUCTURE.md", "CONTRIBUTING.md", "AGENTS.md", "LICENSE"}

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

TYPE_ID_PATTERNS = {
    "daily": re.compile(r"^DAILY-\d{8}$"),
    "capture": re.compile(r"^CAP-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "project": re.compile(r"^PRJ-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "area": re.compile(r"^AREA-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "meeting": re.compile(r"^MTG-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "experiment": re.compile(r"^EXP-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "learning-note": re.compile(r"^LRN-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "literature": re.compile(r"^LIT-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "concept": re.compile(r"^KB-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "decision": re.compile(r"^ADR-\d{8}-\d{6}(?:-[A-Za-z0-9_-]+)?$"),
    "playbook": re.compile(r"^PB-(?:\d{8}-\d{4,6}|\d{8}-[A-Za-z0-9_-]+)$"),
    "specification": re.compile(r"^META-[A-Z0-9_-]+$"),
    "profile": re.compile(r"^META-[A-Z0-9_-]+$"),
}

AGENT_ID_PATTERNS = [
    # UUIDv4
    re.compile(r"^[A-Z]+-[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"),
    # ULID
    re.compile(r"^[A-Z]+-[0-9A-HJ-KM-NP-TV-Z]{26}$"),
]

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
    "profile": {"draft", "active"},
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

def render_template_frontmatter(raw_fm: str) -> str:
    """Render template placeholders with deterministic dummy values for schema checking."""
    substitutions = [
        (r"\{\{title\}\}", "Sample Title"),
        (r"\{\{date\}\}", "2026-01-01"),
        (r"\{\{time\}\}", "12:00:00"),
        (r"\{\{date:YYYY\}\}", "2026"),
        (r"\{\{date:MM\}\}", "01"),
        (r"\{\{date:dddd\}\}", "Thursday"),
        (r"\{\{date:YYYYMMDD\}\}", "20260101"),
        (r"\{\{time:HHmmss\}\}", "120000"),
    ]
    rendered = raw_fm
    for pat, repl in substitutions:
        rendered = re.sub(pat, repl, rendered)
    return rendered

def validate_single_frontmatter(data: dict, rel_posix: str) -> list:
    """Validate a parsed frontmatter dictionary against the canonical schema."""
    errors = []

    # 1. Base required fields check for all notes (id, type, tags)
    if "id" not in data or not data["id"]:
        errors.append(f"[Missing ID] {rel_posix}: Missing required 'id' frontmatter field.")
        return errors

    note_id = str(data["id"]).strip()

    if "type" not in data or not data["type"]:
        errors.append(f"[Missing Type] {rel_posix}: Missing required 'type' frontmatter field.")
        return errors

    note_type = str(data["type"]).strip()
    if note_type not in VALID_NOTE_TYPES:
        errors.append(f"[Invalid Type] {rel_posix}: Unknown note type '{note_type}'.")
        return errors

    if "tags" not in data or data["tags"] is None:
        errors.append(f"[Missing Tags] {rel_posix}: Missing required 'tags' frontmatter field.")
    elif not isinstance(data["tags"], list):
        errors.append(f"[Malformed Tags] {rel_posix}: 'tags' must be a YAML list.")
    elif len(data["tags"]) == 0:
        errors.append(f"[Empty Tags] {rel_posix}: 'tags' list must contain at least one tag.")
    else:
        for tag in data["tags"]:
            if not isinstance(tag, str) or not tag.strip():
                errors.append(f"[Malformed Tag] {rel_posix}: All tags must be non-empty strings.")
                break

    # 2. Check Type-Specific ID Prefix
    expected_prefix = TYPE_PREFIX_MAP.get(note_type)
    if expected_prefix and not note_id.startswith(expected_prefix):
        errors.append(
            f"[Prefix Mismatch] {rel_posix}: Note type '{note_type}' requires ID prefix '{expected_prefix}', got '{note_id}'."
        )

    # 3. Check ID Pattern (Full format or agent UUID/ULID)
    id_pattern = TYPE_ID_PATTERNS.get(note_type)
    if id_pattern:
        matches_pattern = id_pattern.match(note_id) is not None
        matches_agent = any(pat.match(note_id) is not None for pat in AGENT_ID_PATTERNS)
        if not (matches_pattern or matches_agent):
            errors.append(
                f"[Malformed ID Pattern] {rel_posix}: ID '{note_id}' does not match canonical pattern for type '{note_type}'."
            )

    # 4. Check Type-Specific Required Fields
    req_fields = TYPE_REQUIRED_FIELDS.get(note_type, [])
    for field in req_fields:
        if field not in data or data[field] is None or data[field] == "":
            errors.append(f"[Missing Field] {rel_posix}: Note type '{note_type}' requires '{field}' frontmatter field.")

    # 5. Check Allowed Enums
    if note_type in ALLOWED_STATUS and "status" in data and data["status"]:
        if str(data["status"]).strip() not in ALLOWED_STATUS[note_type]:
            errors.append(
                f"[Invalid Status] {rel_posix}: Status '{data['status']}' is invalid for type '{note_type}'. "
                f"Allowed: {sorted(ALLOWED_STATUS[note_type])}"
            )

    if "reading_status" in data and data["reading_status"]:
        if str(data["reading_status"]).strip() not in ALLOWED_READING_STATUS:
            errors.append(
                f"[Invalid Reading Status] {rel_posix}: Reading status '{data['reading_status']}' is invalid. "
                f"Allowed: {sorted(ALLOWED_READING_STATUS)}"
            )

    if "confidence" in data and data["confidence"]:
        if str(data["confidence"]).strip() not in ALLOWED_CONFIDENCE:
            errors.append(
                f"[Invalid Confidence] {rel_posix}: Confidence '{data['confidence']}' is invalid. "
                f"Allowed: {sorted(ALLOWED_CONFIDENCE)}"
            )

    # 6. Check Field Types and Formats
    if "date" in data and data["date"] is not None:
        val = str(data["date"]).strip()
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", val):
            errors.append(f"[Invalid Date Format] {rel_posix}: 'date' must be in YYYY-MM-DD format, got '{val}'.")

    if "year" in data and data["year"] is not None:
        val = str(data["year"]).strip()
        if not re.match(r"^\d{4}$", val):
            errors.append(f"[Invalid Year Format] {rel_posix}: 'year' must be a 4-digit year, got '{val}'.")

    if "rag_include" in data and not isinstance(data["rag_include"], bool):
        errors.append(f"[Invalid Type] {rel_posix}: 'rag_include' must be a boolean (true/false).")

    if "aliases" in data and not isinstance(data["aliases"], list):
        errors.append(f"[Invalid Type] {rel_posix}: 'aliases' must be a YAML list.")

    if "sources" in data and not isinstance(data["sources"], list):
        errors.append(f"[Invalid Type] {rel_posix}: 'sources' must be a YAML list.")

    return errors

def validate_templates(vault_dir: Path):
    """Validate template variable syntax and template frontmatter schemas."""
    errors = []
    templates_dir = vault_dir / "templates"
    if not templates_dir.exists():
        return errors

    var_pattern = re.compile(r"\{\{([^}]+)\}\}")

    for file_path in sorted(templates_dir.glob("*.md")):
        rel_posix = file_path.relative_to(vault_dir).as_posix()
        content = file_path.read_text(encoding="utf-8")

        # 1. Variable check
        matches = var_pattern.findall(content)
        for var in matches:
            var_clean = var.strip()
            if var_clean in ALLOWED_CORE_VARS:
                continue
            if ALLOWED_MOMENT_FORMATS.match(var_clean):
                continue
            errors.append(
                f"[Template Syntax Error] {rel_posix}: "
                f"Unsupported template variable '{{{{{var}}}}}'. Only Obsidian Core variables and Moment formatters are permitted."
            )

        # 2. Frontmatter schema check with safe substitution
        raw_fm = extract_frontmatter(content)
        if raw_fm is None:
            errors.append(f"[Missing Frontmatter] {rel_posix}: Template lacks YAML frontmatter delimiters ('---').")
            continue

        rendered_fm = render_template_frontmatter(raw_fm)
        try:
            data = yaml.safe_load(rendered_fm)
        except yaml.YAMLError as exc:
            errors.append(f"[Template YAML Error] {rel_posix}: Failed to parse frontmatter after variable substitution: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"[Template Malformed] {rel_posix}: Template frontmatter is not a key-value mapping.")
            continue

        fm_errors = validate_single_frontmatter(data, rel_posix)
        errors.extend(fm_errors)

    return errors

def validate_frontmatter(vault_dir: Path):
    """Validate YAML frontmatter and ID uniqueness across all markdown files (excluding templates)."""
    errors = []
    seen_ids = {}
    
    for file_path in sorted(vault_dir.rglob("*.md")):
        rel_path = file_path.relative_to(vault_dir)
        rel_posix = rel_path.as_posix()
        
        # Skip templates folder and dot-directories using path parts
        if (rel_path.parts and rel_path.parts[0] == "templates") or any(part.startswith(".") for part in rel_path.parts):
            continue

        content = file_path.read_text(encoding="utf-8")
        raw_fm = extract_frontmatter(content)
        
        if raw_fm is None:
            # Informational READMEs without frontmatter are permitted
            if file_path.name in FRAMEWORK_DOC_FILES or file_path.name == "README.md":
                continue
            errors.append(f"[Missing Frontmatter] {rel_posix}: Note lacks valid YAML frontmatter delimiters ('---').")
            continue

        try:
            data = yaml.safe_load(raw_fm)
        except yaml.YAMLError as exc:
            errors.append(f"[YAML Syntax Error] {rel_posix}: Failed to parse YAML frontmatter: {exc}")
            continue

        if not isinstance(data, dict):
            errors.append(f"[Malformed Frontmatter] {rel_posix}: Frontmatter is not a key-value mapping.")
            continue

        # Check ID uniqueness across entire vault
        note_id = str(data.get("id", "")).strip()
        if note_id:
            if note_id in seen_ids:
                errors.append(f"[Duplicate ID] {rel_posix}: ID '{note_id}' is already used by '{seen_ids[note_id]}'.")
            else:
                seen_ids[note_id] = rel_posix

        file_errors = validate_single_frontmatter(data, rel_posix)
        errors.extend(file_errors)

    return errors

def validate_wikilinks(vault_dir: Path):
    """Perform three-tier wikilink verification with cross-platform path normalization and asset support."""
    errors = []
    warnings = []

    # Map existing files by filename, stem, and POSIX relative paths
    existing_targets = set()
    for f in vault_dir.rglob("*"):
        if not f.is_file() or any(part.startswith(".") for part in f.parts):
            continue
        rel_posix = f.relative_to(vault_dir).as_posix()
        existing_targets.add(f.name)
        existing_targets.add(f.stem)
        existing_targets.add(rel_posix)
        if f.suffix == ".md":
            existing_targets.add(rel_posix[:-3])

    wikilink_pattern = re.compile(r"\[\[([^\]]+)\]\]")

    for file_path in sorted(vault_dir.rglob("*.md")):
        rel_path = file_path.relative_to(vault_dir)
        rel_posix = rel_path.as_posix()

        if any(part.startswith(".") for part in rel_path.parts):
            continue

        # Ignore templates/ for broken link checks
        if rel_path.parts and rel_path.parts[0] == "templates":
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

            # Reject absolute or drive-qualified paths
            if target.startswith("/") or target.startswith("\\") or re.match(r"^[A-Za-z]:", target):
                errors.append(f"[Security Error] {rel_posix}: Absolute path in link '{raw_link}' is forbidden.")
                continue

            # Check for path traversal escaping vault
            try:
                resolved_target = (vault_dir / target).resolve()
                if not resolved_target.is_relative_to(vault_dir.resolve()):
                    errors.append(f"[Security Error] {rel_posix}: Link '{raw_link}' attempts path traversal.")
                    continue
            except Exception:
                errors.append(f"[Security Error] {rel_posix}: Invalid link path '{raw_link}'.")
                continue

            # Strip .md suffix if present
            target_clean = target[:-3] if target.endswith(".md") else target

            # Check if target exists in vault
            exists = (
                target in existing_targets or
                target_clean in existing_targets or
                (vault_dir / f"{target_clean}.md").exists()
            )

            if not exists:
                msg = f"{rel_posix}: Unresolved wikilink target '[[{target}]]'"
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
    print("[1/3] Validating template variables & schemas...")
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

from pathlib import Path
from datetime import date

# =========================
# KONFIGURATION
# =========================
VERSION = "4.2.0-RECURSIVE"
IGNORE_FILES = {"desktop.ini", "thumbs.db", ".ds_store"}
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".obsidian", ".trash"}
ICONS = ["🜁", "🜂", "🜃", "🜄", "🜅"]

ROOT = Path.cwd().resolve()
MASTER_INDEX_NAME = f"{ROOT.name}.Start.md"

# =========================
# HJÄLPFUNKTIONER
# =========================
def slugify(text: str) -> str:
    return text.lower().replace(" ", "-").replace("/", "-")

def inject_yaml(file_path: Path, depth: int):
    """Lägg till YAML-frontmatter om den saknas."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return

    if content.startswith("---"):
        return

    icon = ICONS[min(depth, len(ICONS) - 1)]
    rel = file_path.relative_to(ROOT)

    yaml = f"""---
id: {slugify(str(rel.with_suffix('')))}
type: document
title: "{file_path.stem}"
icon: "{icon}"
depth: {depth}
created: {date.today()}
tags: [navigation]
---

"""
    file_path.write_text(yaml + content, encoding="utf-8")

def ensure_anchor_file(folder: Path) -> Path:
    """Skapar en Start-fil för mappen om den inte finns."""
    anchor_name = f"{folder.name}.Start.md"
    anchor_path = folder / anchor_name

    if anchor_path.exists():
        return anchor_path

    content = f"""--- 
type: anchor
role: start
folder: "{folder.name}"
---

"""
    anchor_path.write_text(content, encoding="utf-8")
    return anchor_path

# =========================
# BYGG START-FILER REKURSIVT
# =========================
def build_start(folder: Path, depth: int = 0):
    """
    Skapar Start-fil för mappen och undermappar rekursivt.
    """
    # Hitta alla objekt i mappen
    items = sorted(folder.iterdir(), key=lambda x: (not x.is_dir(), x.name.lower()))

    # Skapa Start-fil
    anchor_path = ensure_anchor_file(folder)
    lines = []

    # Header enligt mall
    icon = ICONS[min(depth, len(ICONS) - 1)]
    lines.append(f">````Python\n>\n>{folder.name} {icon} CorePro ⌖ — ⊕ Nav.3.0\n>\n>````\n")
    lines.append(f"# $$\\boxed{{RP9_\\sqrt{{\\mathrm{{META}}}}}}$$\n")
    lines.append("---\n\n")

    # Bygg fil- och mapplista med vänsterlinjer och tomrader
    for item in items:
        if item.name.lower() in IGNORE_FILES or item.name in IGNORE_DIRS:
            continue

        if item.is_dir():
            # Länk till Start-fil i undermappen
            sub_anchor = build_start(item, depth + 1)
            rel_sub_anchor = sub_anchor.relative_to(ROOT).as_posix()[:-3]

            lines.append("│")
            lines.append("│")
            lines.append(f"│- 📂 **{item.name}**")
            lines.append(f"│  - 📄 [[{rel_sub_anchor}|{item.name}.Start]]")
            lines.append("│")
            lines.append("│")
            lines.append("│")

        elif item.suffix.lower() == ".md":
            inject_yaml(item, depth + 1)
            rel = item.relative_to(ROOT).as_posix()[:-3]
            lines.append("│")
            lines.append("│")
            lines.append(f"- 📄 [[{rel}|{item.stem}]]")
            lines.append("│")
            lines.append("│")

    # Skriv Start-fil
    anchor_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ {anchor_path.relative_to(ROOT)} skapad")

    return anchor_path

# =========================
# GENERERA ROOT.START.MD
# =========================
def generate_root():
    build_start(ROOT)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    generate_root()

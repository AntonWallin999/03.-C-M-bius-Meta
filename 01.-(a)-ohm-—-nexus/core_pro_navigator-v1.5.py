from pathlib import Path
from datetime import date

# =========================
# KONFIGURATION
# =========================
VERSION = "4.3.0-STANDARDIZED"
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

# =========================
# BYGG STARTFIL (REKURSIVT)
# =========================
def build_start_file(folder: Path, depth: int = 0):
    anchor = folder / f"{folder.name}.Start.md"

    lines = [
        ">````Python",
        ">",
        f">{folder.name} {ICONS[min(depth, len(ICONS)-1)]} CorePro ⌖ — ⊕ Nav.3.0",
        ">",
        ">````",
        "",
        "# $$\\boxed{RP9_\\sqrt{\\mathrm{META}}}$$",
        "",
        "---",
        "",
    ]

    items = sorted(
        [i for i in folder.iterdir() if i.name not in IGNORE_FILES and i.name not in IGNORE_DIRS],
        key=lambda x: (not x.is_dir(), x.name.lower())
    )

    counter = 1
    first = True

    for item in items:
        if item == anchor:
            continue

        if not first:
            lines.extend(["│", "│"])
        first = False

        prefix = f"{counter}. - "
        counter += 1

        if item.is_dir():
            sub_anchor = build_start_file(item, depth + 1)
            rel = sub_anchor.relative_to(ROOT).as_posix()[:-3]
            lines.append(f"- **{prefix}**📂 [[{rel}|{item.name}]]")

        elif item.suffix.lower() == ".md":
            inject_yaml(item, depth + 1)
            rel = item.relative_to(ROOT).as_posix()[:-3]
            lines.append(f"- **{prefix}**📄 [[{rel}|{item.stem}]]")

    anchor.write_text("\n".join(lines), encoding="utf-8")
    print(f"✅ {anchor.relative_to(ROOT)}")

    return anchor

# =========================
# GENERERA ROOT
# =========================
def generate():
    build_start_file(ROOT)

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    generate()

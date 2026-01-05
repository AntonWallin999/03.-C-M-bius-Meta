import os
from pathlib import Path
import re

# Inställningar
INDEX_NAME = "i.md"
MASTER_INDEX_NAME = "START.md"
VERSION = "2.1.0-GH-HTML"

# Filer och mappar som ska ignoreras
IGNORE_FILES = {INDEX_NAME.lower(), MASTER_INDEX_NAME.lower(), "desktop.ini", "thumbs.db", ".ds_store"}
IGNORE_EXTENSIONS = {".py", ".pyc"}
IGNORE_DIRS = {".git", "__pycache__", "node_modules", ".obsidian", ".trash"}

def safe_iterdir(path: Path):
    try:
        return list(path.iterdir())
    except Exception:
        return []

def inject_yaml_to_file(file_path: Path, depth: int):
    """Injekterar YAML frontmatter i en befintlig Markdown-fil."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return

    ICONS = ["🜁", "🜂", "🜃", "🜄", "🜅"]
    icon = ICONS[min(depth, len(ICONS) - 1)]
    
    yaml_frontmatter = f"""---
# ========== IDENTITET (unika per dokument) ==========
id: "{file_path.stem.lower().replace(' ', '-')}"
type: "document"
title: "{file_path.stem}"
subjekt: "{icon}. RP9 Swe"
author: "Anton Wallin"
date: 2025-08-09
version: "1.0"
series: "#{icon}. RP9"
part: "Del av {file_path.parent.name}"
doc_type: "Data"
---

"""
    if content.startswith("---"):
        end_idx = content.find("---", 3)
        if end_idx != -1:
            new_content = yaml_frontmatter + content[end_idx + 3:].lstrip()
        else:
            new_content = yaml_frontmatter + content
    else:
        new_content = yaml_frontmatter + content

    file_path.write_text(new_content, encoding="utf-8")

def generate_master_index(root_path: Path, folders, files):
    """Skapar en unik startsida med HTML-utfällning för GitHub."""
    lines = []
    lines.append("---")
    lines.append(f"id: 00")
    lines.append(f"type: master-root")
    lines.append(f"navigation: \"🜁 — RP9 Master Index V: {VERSION}\"")
    lines.append(f"author: \"Anton Wallin\"")
    lines.append("---")
    lines.append("")
    # HTML ERSÄTTNING FÖR CALLOUT
    lines.append("<details open>")
    lines.append("<summary><b>- - - = ( MASTER INDEX ) = - - -</b></summary>")
    lines.append("")
    lines.append("> ---")
    lines.append(">")
    lines.append("> <br />")
    lines.append(">")
    lines.append(f"> # 💠 {root_path.name} — Systemkatalog")
    lines.append(">")
    lines.append("> ---")
    lines.append(">")
    lines.append("> <br />")
    lines.append(">")
    lines.append("> ## 📂 Huvudkategorier")
    lines.append(">")
    lines.append("> ---")
    lines.append(">")
    
    if folders:
        for folder in folders:
            lines.append(f"> ### 🔗 [{folder.name}]({folder.name}/{INDEX_NAME})")
            lines.append(">")
            lines.append("> ---")
            lines.append(">")
    
    lines.append("> <br />")
    lines.append(">")
    lines.append("> ## 📄 Rot-filer")
    lines.append(">")
    lines.append("> ---")
    lines.append(">")
    if files:
        for file in files:
            lines.append(f"> - 📄 [{file.name}]({file.name})")
    else:
        lines.append("> *Inga filer i roten.*")
    
    lines.append(">")
    lines.append("> <br />")
    lines.append(">")
    lines.append(">---")
    lines.append(">")
    lines.append(">````python")
    lines.append("> 📊 System Metadata")
    lines.append(f"> 📁 Topp-mappar: {len(folders)}")
    lines.append(f"> 📄 Filer i rot: {len(files)}")
    lines.append("> ````")
    lines.append(">")
    lines.append(">---")
    lines.append("</details>") # SLUT PÅ HTML
    lines.append("")
    lines.append(".")
    
    (root_path / MASTER_INDEX_NAME).write_text("\n".join(lines), encoding="utf-8")

def generate_index(dir_path: Path, root: Path, current_id: str = "00"):
    folders = []
    files = []
    docs = []

    for item in safe_iterdir(dir_path):
        name_lower = item.name.lower()
        if name_lower in IGNORE_FILES or item.is_symlink():
            continue
        if item.suffix.lower() in IGNORE_EXTENSIONS:
            continue

        if item.is_dir():
            if name_lower in IGNORE_DIRS:
                continue
            folders.append(item)
        elif item.is_file():
            if item.suffix.lower() == ".md":
                root_parts = root.resolve().parts
                dir_parts = dir_path.resolve().parts
                depth = len(dir_parts) - len(root_parts)
                inject_yaml_to_file(item, depth)

            if name_lower == "readme.md" or name_lower == "index.md":
                docs.append(item)
            else:
                files.append(item)

    folders.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())
    docs.sort(key=lambda x: x.name.lower())

    if dir_path == root:
        generate_master_index(dir_path, folders, files)

    root_parts = root.resolve().parts
    dir_parts = dir_path.resolve().parts
    depth = len(dir_parts) - len(root_parts)
    
    ICONS = ["🜁", "🜂", "🜃", "🜄", "🜅"]
    icon = ICONS[min(depth, len(ICONS) - 1)]

    lines = []
    lines.append("---")
    lines.append(f"id: {current_id}")
    lines.append(f"level: {depth}")
    lines.append(f"name: \"{dir_path.name}\"")
    lines.append(f"navigation: \"{icon} — RP9Cor£Pro V: {VERSION}\"")
    lines.append(f"subjekt: \"{icon}. RP9 Swe\"")
    lines.append(f"author: \"Anton Wallin\"")
    lines.append("---")
    lines.append("")
    # HTML ERSÄTTNING FÖR CALLOUT
    lines.append("<details open>")
    lines.append(f"<summary><b>- - - = ( RP9 : {dir_path.name} ) = - - -</b></summary>")
    lines.append("")
    lines.append("> ---")
    lines.append(">")
    lines.append("> <br />")
    lines.append(">")
    lines.append(f"> # {dir_path.name}")
    lines.append(">")
    lines.append("> ---")
    lines.append(">")
    lines.append("> <br />")
    lines.append(">")
    
    if docs:
        lines.append(f"> #  **ⓘ-®-{icon}**")
        lines.append(">")
        lines.append("> ---")
        lines.append(">")
        for doc in docs:
            lines.append(f">>> #### 🔗 [{doc.name}]({doc.name})")
            lines.append(">>>")
            lines.append(">>> ---")
            lines.append(">>>")
        lines.append("> <br />")
        lines.append(">")

    lines.append(f"> ## **ⓘ** : {dir_path.name} ")
    lines.append(">")
    lines.append(">---")
    lines.append(">")
    lines.append("> ####  *Filer* 📓")
    lines.append(">") 
    
    if files:
        lines.append(">> ---")
        lines.append(">>")
        for i, file in enumerate(files, start=1):
            lines.append(f">>> #### {i:02d}. 📄 [{file.name}]({file.name})")
            lines.append(">>>")
            lines.append(">>> ---")
            lines.append(">>>")
    else:
        lines.append(">> *Inga filer funna.*")

    lines.append(">")
    lines.append("> <br />")
    lines.append(">")
    
    if folders:
        lines.append("> #### *Mappar* 📂")
        lines.append(">")
        lines.append("> ---")
        lines.append(">")
        lines.append(">> ---")
        lines.append(">>")
        for i, folder in enumerate(folders, start=1):
            lines.append(f">>> #### {i:02d}. 🔗 [{folder.name}]({folder.name}/{INDEX_NAME})")
            lines.append(">>>")
            lines.append(">>> ---")
            lines.append(">>>")

    lines.append(">")
    lines.append("> <br />")
    lines.append(">")

    if depth > 0:
        lines.append("> ---")
        lines.append(">")
        lines.append(f"> ### ⬆️ [Upp](../{INDEX_NAME})")
        lines.append(">")
        if depth == 1:
            lines.append(f"> ### 🏠 [Hem till Master Index]({MASTER_INDEX_NAME})")
            lines.append(">")
        lines.append("> ---")
        lines.append(">")
    
    lines.append("> <br />")
    lines.append(">")
    lines.append("> ---")
    lines.append(">")
    lines.append(">## **📁** *Vidare*")
    lines.append(">")
    lines.append("> ---")
    lines.append(">")

    if folders:
        for i, folder in enumerate(folders):
            indent_prefix = ">" * (i + 1)
            lines.append(f"{indent_prefix}#### -  **L{i+2}.📂** [{folder.name}]({folder.name}/{INDEX_NAME})")
            lines.append(f"{indent_prefix}")
            lines.append(f"{indent_prefix}---")
            lines.append(f"{indent_prefix}")
    
    lines.append(">````python")
    lines.append("> 📊 Metadata")
    lines.append(f"> 📁 Mappar: {len(folders)}")
    lines.append(f"> 📄 Filer: {len(files)}")
    lines.append("> ````")
    lines.append(">")
    
    long_sep = ">" * 27 + "---"
    lines.append(long_sep)
    lines.append(">")
    
    relative_parts = dir_parts[len(root_parts):]
    breadcrumb = "root" + (" / " + " / ".join(relative_parts) if relative_parts else "")

    lines.append(">````python")
    lines.append("> 📍 GPS Positionering")
    lines.append(f"> Path: {breadcrumb}")
    lines.append(f"> Level: {depth}")
    lines.append("> ````")
    lines.append(">")
    lines.append(long_sep)
    lines.append(">")
    lines.append(">````")
    lines.append(f">Navigation: {icon} — RP9Cor£Pro  V: {VERSION}")
    lines.append(f">ID: {current_id}")
    lines.append(">````")
    lines.append("---")
    lines.append("</details>") # SLUT PÅ HTML
    lines.append("")
    lines.append(".")

    (dir_path / INDEX_NAME).write_text("\n".join(lines), encoding="utf-8")

def recurse(dir_path: Path, root: Path, visited: set, parent_id: str = "00"):
    real = dir_path.resolve()
    if real in visited:
        return
    visited.add(real)
    generate_index(dir_path, root, parent_id)
    sub_folders = [f for f in safe_iterdir(dir_path) if f.is_dir() and f.name.lower() not in IGNORE_DIRS and not f.is_symlink()]
    sub_folders.sort(key=lambda x: x.name.lower())
    for i, item in enumerate(sub_folders):
        recurse(item, root, visited, f"{parent_id}.{i+1}")

if __name__ == "__main__":
    start_node = Path.cwd().resolve()
    recurse(start_node, start_node, set(), "00")
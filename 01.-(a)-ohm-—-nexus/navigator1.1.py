from pathlib import Path

ROOT = Path.cwd().resolve()

LEVEL_0_FILE = "START.md"
LEVEL_1_FILE = "START_LEVEL_1.md"
LEVEL_2_FILE = "START_LEVEL_2.md"

IGNORE_DIRS = {
    ".git",
    ".obsidian",
    ".trash",
    "__pycache__"
}

# ------------------------------
# NIVÅ 2 – DOKUMENT
# ------------------------------

def generate_level_2(subfolder: Path) -> bool:
    documents = [
        f for f in subfolder.iterdir()
        if f.is_file()
        and f.suffix == ".md"
        and f.name not in {LEVEL_1_FILE, LEVEL_2_FILE, LEVEL_0_FILE}
    ]

    if not documents:
        return False

    content = [
        "# 📄 Dokument",
        ""
    ]

    for doc in sorted(documents):
        content.append(f"- [[{doc.stem}]]")

    (subfolder / LEVEL_2_FILE).write_text(
        "\n".join(content),
        encoding="utf-8"
    )
    return True


# ------------------------------
# NIVÅ 1 – UNDERMAPpar
# ------------------------------

def generate_level_1(main_folder: Path) -> bool:
    subfolders = [
        d for d in main_folder.iterdir()
        if d.is_dir() and d.name not in IGNORE_DIRS
    ]

    links = []

    for sub in sorted(subfolders):
        if generate_level_2(sub):
            links.append(f"- [[{sub.name}/{LEVEL_2_FILE}|📂 {sub.name}]]")

    if not links:
        return False

    content = [
        "# 📁 Undermappar",
        ""
    ] + links

    (main_folder / LEVEL_1_FILE).write_text(
        "\n".join(content),
        encoding="utf-8"
    )
    return True


# ------------------------------
# NIVÅ 0 – ROT
# ------------------------------

def generate_level_0():
    main_folders = [
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name not in IGNORE_DIRS
    ]

    content = [
        "# 💠 SYSTEM MASTER INDEX",
        ""
    ]

    for main in sorted(main_folders):
        if generate_level_1(main):
            content.append(
                f"- [[{main.name}/{LEVEL_1_FILE}|📁 {main.name}]]"
            )

    (ROOT / LEVEL_0_FILE).write_text(
        "\n".join(content),
        encoding="utf-8"
    )


if __name__ == "__main__":
    generate_level_0()
    print("✅ Obsidian-kompatibelt fraktalt navigationssystem skapat")
from pathlib import Path

ROOT = Path.cwd().resolve()

LEVEL_0_FILE = "START.md"
LEVEL_1_FILE = "START_LEVEL_1.md"
LEVEL_2_FILE = "START_LEVEL_2.md"

IGNORE_DIRS = {
    ".git",
    ".obsidian",
    ".trash",
    "__pycache__"
}

# ------------------------------
# NIVÅ 2 – DOKUMENT
# ------------------------------

def generate_level_2(subfolder: Path) -> bool:
    documents = [
        f for f in subfolder.iterdir()
        if f.is_file()
        and f.suffix == ".md"
        and f.name not in {LEVEL_1_FILE, LEVEL_2_FILE, LEVEL_0_FILE}
    ]

    if not documents:
        return False

    content = [
        "# 📄 Dokument",
        ""
    ]

    for doc in sorted(documents):
        content.append(f"- [[{doc.stem}]]")

    (subfolder / LEVEL_2_FILE).write_text(
        "\n".join(content),
        encoding="utf-8"
    )
    return True


# ------------------------------
# NIVÅ 1 – UNDERMAPpar
# ------------------------------

def generate_level_1(main_folder: Path) -> bool:
    subfolders = [
        d for d in main_folder.iterdir()
        if d.is_dir() and d.name not in IGNORE_DIRS
    ]

    links = []

    for sub in sorted(subfolders):
        if generate_level_2(sub):
            links.append(f"- [[{sub.name}/{LEVEL_2_FILE}|📂 {sub.name}]]")

    if not links:
        return False

    content = [
        "# 📁 Undermappar",
        ""
    ] + links

    (main_folder / LEVEL_1_FILE).write_text(
        "\n".join(content),
        encoding="utf-8"
    )
    return True


# ------------------------------
# NIVÅ 0 – ROT
# ------------------------------

def generate_level_0():
    main_folders = [
        d for d in ROOT.iterdir()
        if d.is_dir() and d.name not in IGNORE_DIRS
    ]

    content = [
        "# 💠 SYSTEM MASTER INDEX",
        ""
    ]

    for main in sorted(main_folders):
        if generate_level_1(main):
            content.append(
                f"- [[{main.name}/{LEVEL_1_FILE}|📁 {main.name}]]"
            )

    (ROOT / LEVEL_0_FILE).write_text(
        "\n".join(content),
        encoding="utf-8"
    )


if __name__ == "__main__":
    generate_level_0()
    print("✅ Obsidian-kompatibelt fraktalt navigationssystem skapat")

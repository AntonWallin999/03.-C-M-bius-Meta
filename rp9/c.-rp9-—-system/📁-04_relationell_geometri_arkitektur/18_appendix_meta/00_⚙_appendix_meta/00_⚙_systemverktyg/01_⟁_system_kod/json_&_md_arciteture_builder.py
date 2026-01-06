import os
import json

# -------------------------------------------------
# Självmedveten kontext
# -------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# -------------------------------------------------
# Hitta exakt EN json och EN md i samma katalog
# -------------------------------------------------
json_files = [f for f in os.listdir(SCRIPT_DIR) if f.lower().endswith(".json")]
md_files = [f for f in os.listdir(SCRIPT_DIR) if f.lower().endswith(".md")]

if len(json_files) != 1:
    raise RuntimeError(
        f"Fel: förväntade exakt 1 .json-fil, hittade {len(json_files)}:\n{json_files}"
    )

if len(md_files) != 1:
    raise RuntimeError(
        f"Fel: förväntade exakt 1 .md-fil, hittade {len(md_files)}:\n{md_files}"
    )

JSON_PATH = os.path.join(SCRIPT_DIR, json_files[0])
MD_PATH = os.path.join(SCRIPT_DIR, md_files[0])

# Appendix-roten får namn från JSON-filen (utan ändelse)
APPENDIX_ROOT = os.path.join(
    SCRIPT_DIR, os.path.splitext(json_files[0])[0]
)

# -------------------------------------------------
# Hjälpfunktioner
# -------------------------------------------------
def write_index(path, title, entries):
    index_path = os.path.join(path, "INDEX.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(f"# {title}\n\n")
        for name in entries:
            f.write(f"- [{name}](./{name})\n")

def build_tree(base_path, tree):
    os.makedirs(base_path, exist_ok=True)
    entries = []

    for name, subtree in tree.items():
        entries.append(name)
        sub_path = os.path.join(base_path, name)

        if isinstance(subtree, dict):
            build_tree(sub_path, subtree)
        else:
            os.makedirs(sub_path, exist_ok=True)

    write_index(base_path, os.path.basename(base_path), entries)

# -------------------------------------------------
# MAIN
# -------------------------------------------------
with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if len(data) != 1:
    raise RuntimeError(
        "JSON-strukturen måste ha exakt en rot-nyckel."
    )

root_name = list(data.keys())[0]
root_tree = data[root_name]

build_tree(APPENDIX_ROOT, root_tree)

# -------------------------------------------------
# Skapa ROT-INDEX.md (överordnad)
# -------------------------------------------------
root_index_path = os.path.join(APPENDIX_ROOT, "INDEX.md")
with open(root_index_path, "w", encoding="utf-8") as f:
    f.write(f"# {root_name} – Rotindex\n\n")
    f.write(f"> Dokumentation: {md_files[0]}\n\n")
    for name in root_tree.keys():
        f.write(f"- [{name}](./{name})\n")

# -------------------------------------------------
# Rapport
# -------------------------------------------------
print("✅ Appendix byggt korrekt.")
print("📁 Rot:", APPENDIX_ROOT)
print("🧱 Struktur från:", json_files[0])
print("📘 Dokumentation:", md_files[0])
print("🧭 Alla INDEX.md genererade.")

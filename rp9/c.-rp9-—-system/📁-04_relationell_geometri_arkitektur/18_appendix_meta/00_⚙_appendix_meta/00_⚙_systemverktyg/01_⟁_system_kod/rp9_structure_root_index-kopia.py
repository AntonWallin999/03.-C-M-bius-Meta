import os

BASE_DIR = "Relationell_Geometri_Arkitektur"

FOLDERS = [
    "00_Summa_ur_FRC_Intro",
    "01_Domanpolicy_och_Hierarki",
    "02_Vesica_Piscis_Ursprunglig_Relation",
    "03_Fraktal_och_Kausal_Funktion",
    "04_Geometriska_Strukturer_ur_Vesican",
    "05_Matematikens_Fyra_Rum",
    "06_Tal_som_Fraktala_Rorelsetillstand",
    "07_Steg_och_Faslagen_1_7_8_9",
    "08_Bokstaver_som_Relationella_Noder",
    "09_Elektromagnetisk_Realisation",
    "10_Irrationella_Tal_och_Skaloberoende",
    "11_Dimensioner_som_Fraktal_Triad",
    "12_Matematiska_Fusioner_och_Konsekvenser",
    "13_Realisationsmodul_Energi_Fysik_Orbitaler",
    "14_Axiom_och_Satser",
    "15_Matematiska_Lemman_och_Satser",
    "16_Geometriska_Relationella_Lemman_och_Satser",
    "17_Visuell_Presentation",
    "18_Appendix"
]

YAML_TEMPLATE = [
    "---",
    "titel: ",
    "domän: ",
    "status: utkast",
    "beroenden: []",
    "version: 0.1",
    "skapad_av: Anton Wallin",
    "system: RP9",
    "---",
    ""
]

def write_file(path, lines=None, overwrite=False):
    if (not overwrite) and os.path.exists(path):
        return
    with open(path, "w", encoding="utf-8") as f:
        if lines:
            for line in lines:
                f.write(line + "\n")

os.makedirs(BASE_DIR, exist_ok=True)

root_index_lines = [
    "# Relationell Geometri – Rotindex",
    "",
    "Bindande navigationsingång.",
    "",
    "## Huvudmappar",
    ""
]

for folder in FOLDERS:
    num = folder.split("_", 1)[0]
    folder_path = os.path.join(BASE_DIR, folder)
    os.makedirs(folder_path, exist_ok=True)

    # --- Tre tomma markdown-alternativ i huvudmappen
    write_file(os.path.join(folder_path, f"A_📕_{folder}.md"))
    write_file(os.path.join(folder_path, f"B_📗_{folder}.md"))
    write_file(os.path.join(folder_path, f"C_📘_{folder}.md"))

    # --- Appendix-mapp: använder bara numret (inte hela mappnamnet)
    appendix_dir_name = f"Appendix_📂_{num}"
    appendix_path = os.path.join(folder_path, appendix_dir_name)
    os.makedirs(appendix_path, exist_ok=True)

    # --- README och YAML i appendix
    readme_short = f"📜_Readme_(Short)_{folder}.md"
    readme_long = f"📜_Readme_(Long)_{folder}.md"

    write_file(
        os.path.join(appendix_path, readme_short),
        [
            f"# 📜 README (Short) – {folder}",
            "",
            "Kort översikt (fylls i)."
        ]
    )

    write_file(
        os.path.join(appendix_path, readme_long),
        [
            f"# 📜 README (Long) – {folder}",
            "",
            "Full strukturell och funktionell beskrivning (fylls i)."
        ]
    )

    write_file(os.path.join(appendix_path, "YAML_Frontmatter.md"), YAML_TEMPLATE)

    # --- INDEX i appendix (länkar till filer i appendix)
    write_file(
        os.path.join(appendix_path, "INDEX.md"),
        [
            f"# INDEX – Appendix – {folder}",
            "",
            f"- [📜 README (Short)](./{readme_short})",
            f"- [📜 README (Long)](./{readme_long})",
            f"- [YAML Frontmatter](./YAML_Frontmatter.md)"
        ],
        overwrite=True
    )

    # --- Root index länkar huvudmapp + appendix index
    root_index_lines.extend([
        f"### {folder}",
        "",
        f"- [Appendix INDEX]({folder}/{appendix_dir_name}/INDEX.md)",
        f"- Huvuddokument:",
        f"  - [A_📕]({folder}/A_📕_{folder}.md)",
        f"  - [B_📗]({folder}/B_📗_{folder}.md)",
        f"  - [C_📘]({folder}/C_📘_{folder}.md)",
        ""
    ])

# --- Root INDEX.md
write_file(os.path.join(BASE_DIR, "INDEX.md"), root_index_lines, overwrite=True)

print("✅ Klar.")
print("✅ Huvudmappnamn oförändrade (FOLDERS används direkt).")
print("✅ Appendix-mappnamn använder endast numret: Appendix_📂_XX")
print("✅ README + YAML ligger i Appendix.")
print("✅ Tre tomma md-alternativ skapade i varje huvudmapp.")
print("✅ Root INDEX.md och Appendix INDEX.md genererade.")
print("📁 Bas:", os.path.abspath(BASE_DIR))

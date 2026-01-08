import os
import json

def get_output_basename(root_dir):
    # Använder namnet på mappen där skriptet körs
    return os.path.basename(root_dir)

def build_index(root_dir, output_md_name):
    index_tree = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Ignonera den nyskapade export-mappen för att undvika att den indexerar sig själv
        if "(F.R.C)" in dirpath:
            continue
            
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir == ".":
            rel_dir = ""
        parts = rel_dir.split(os.sep) if rel_dir else []

        pointer = index_tree
        for part in parts:
            if part not in pointer:
                pointer[part] = {}
            pointer = pointer[part]

        md_files = []
        for filename in sorted(filenames):
            if filename.lower().endswith(".md") and filename != output_md_name:
                md_files.append(filename)

        if md_files:
            pointer["_files"] = md_files

    return index_tree

def merge_markdown_files(root_dir, output_path, output_md_name):
    # Skapar mappen om den inte finns
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as outfile:
        for dirpath, _, filenames in os.walk(root_dir):
            # Hoppa över filer inuti den nyskapade (F.R.C)-mappen
            if "(F.R.C)" in dirpath:
                continue
                
            for filename in sorted(filenames):
                if filename.lower().endswith(".md") and filename != output_md_name:
                    full_path = os.path.join(dirpath, filename)
                    rel_path = os.path.relpath(full_path, root_dir)

                    header = (
                        "\n\n---\n"
                        "# " + rel_path + "\n"
                        "---\n\n"
                    )
                    outfile.write(header)

                    with open(full_path, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n")

    print("Markdown merge klar:", output_path)
    return output_path

def write_json_index(output_path, index_data):
    # Skapar mappen om den inte finns
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as jsonfile:
        json.dump(index_data, jsonfile, indent=4, ensure_ascii=False)

    print("JSON-index skapat:", output_path)
    return output_path

if __name__ == "__main__":
    # Rotmappen där skriptet ligger
    root = os.path.dirname(os.path.abspath(__file__))
    base_name = get_output_basename(root)

    # Definiera den nya mappen: (F.R.C) Mappnamn
    export_folder_name = f"(F.R.C) {base_name}"
    export_path = os.path.join(root, export_folder_name)

    # Filnamn
    output_md_name = base_name + ".md"
    output_json_name = base_name + "_index.json"

    # Fullständiga sökvägar till de nya filerna inuti den nya mappen
    full_md_path = os.path.join(export_path, output_md_name)
    full_json_path = os.path.join(export_path, output_json_name)

    # Kör funktionerna
    merge_markdown_files(root, full_md_path, output_md_name)
    index_data = build_index(root, output_md_name)
    write_json_index(full_json_path, index_data)
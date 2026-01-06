import os
import json


def get_output_basename(root_dir):
    # Use only the name of the folder where the script is executed
    return os.path.basename(root_dir)


def build_index(root_dir, output_md_name):
    index_tree = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
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


def merge_markdown_files(root_dir, output_md_name):
    output_path = os.path.join(root_dir, output_md_name)

    with open(output_path, "w", encoding="utf-8") as outfile:
        for dirpath, _, filenames in os.walk(root_dir):
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


def write_json_index(root_dir, index_data, output_json_name):
    json_path = os.path.join(root_dir, output_json_name)
    with open(json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(index_data, jsonfile, indent=4, ensure_ascii=False)

    print("JSON-index skapat:", json_path)
    return json_path


if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))

    base_name = get_output_basename(root)

    output_md = base_name + ".md"
    output_json = base_name + "_index.json"

    merge_markdown_files(root, output_md)
    index_data = build_index(root, output_md)
    write_json_index(root, index_data, output_json)

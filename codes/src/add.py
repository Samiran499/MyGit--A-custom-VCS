import os
import hashlib
from src.root_finder import get_repo_root, normalize_path

def hash_content(filepath):
    with open(filepath, "rb") as file:
        content = file.read()
    return hashlib.sha1(content).hexdigest(), content

def add(filenames): #filenames should be a list
    repo_root = get_repo_root()

    INDEX_FILE = os.path.join(repo_root, ".mygit/index")
    OBJECTS_DIR = os.path.join(repo_root, ".mygit/objects")

    if not os.path.exists(os.path.join(repo_root, ".mygit")):
        print("ERROR: NOT a mygit repository.\nRUN \'mygit init\' first.")
        return
    
    index_entries = {}
    
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as indices:
            for line in indices:
                file, sha1 = line.strip().split()
                index_entries[file] = sha1

        for file in filenames:
            rel_path = normalize_path(file)
            abs_path = os.path.join(repo_root, rel_path)
            if not os.path.exists(file):
                print(F"WARNING: {file} not found :(")
                continue
            sha1, content = hash_content(file)
            obj_path = os.path.join(OBJECTS_DIR, sha1)

            if not os.path.exists(obj_path):
                with open(obj_path, "wb") as obj_file:
                    obj_file.write(content)

            index_entries[rel_path] = sha1
            print(f"STAGED {file}. Hash preview: {sha1[:7]}")

            with open(INDEX_FILE, "w") as indices:
                for rel_path, sha1 in index_entries.items():
                    indices.write(f"{rel_path} {sha1}\n")

import os
import hashlib

INDEX_FILE = ".mygit/index"
OBJECTS_DIR = ".mygit/objects"

def hash_content(filepath):
    with open(filepath, "rb") as file:
        content = file.read()
    return hashlib.sha1(content).hexdigest(), content

def add(filenames): #filenames should be a list
    if not os.path.exists(".mygit"):
        print("ERROR: NOT a mygit repository.\nRUN \'mygit init\' first.")
        return
    
    index_entries = {}
    
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as indices:
            for line in indices:
                file, sha1 = line.strip().split()
                index_entries[file] = sha1

        for file in filenames:
            if not os.path.exists(file):
                print(F"WARNING: {file} not found :(")
                continue
            sha1, content = hash_content(file)
            obj_path = os.path.join(OBJECTS_DIR, sha1)

            if not os.path.exists(obj_path):
                with open(obj_path, "wb") as obj_file:
                    obj_file.write(content)

            index_entries[file] = sha1
            print(f"STAGED {file}. Hash preview: {sha1[:7]}")

            with open(INDEX_FILE, "w") as indices:
                for file, sha1 in index_entries.items():
                    indices.write(f"{file} {sha1}\n")

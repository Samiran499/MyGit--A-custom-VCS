import os
import hashlib

INDEX_FILE = ".mygit/index"
OBJECTS_DIR = ".mygit/objects"

def commit(message = "No message"):
    if not os.path.exists(INDEX_FILE):
        print("No files staged")
        return
    
    with open(INDEX_FILE, "r") as indices_file:
        indices = indices_file.read()

    if not indices.strip():
        print("Staging area empty!")
        return
    
    indices += f"\n message: {message}"
    
    commit_hash = hashlib.sha1(indices.encode()).hexdigest()

    with open(f".mygit/objects/{commit_hash}", "w") as f:
        f.write(indices)

    with open(".mygit/HEAD", "w") as f:
        f.write(commit_hash)

    open(".mygit/index", "w").close()
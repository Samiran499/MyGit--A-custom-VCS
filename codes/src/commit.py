import os
import hashlib
from datetime import datetime
from src.root_finder import get_repo_root

def commit(message = "No message"):
    repo_root = get_repo_root()
    
    INDEX_FILE = os.path.join(repo_root, ".mygit/index")
    OBJECTS_DIR = os.path.join(repo_root, ".mygit/objects")
    HEAD_DIR = os.path.join(repo_root, ".mygit/HEAD")

    if not os.path.exists(INDEX_FILE):
        print("No files staged")
        return
    
    with open(INDEX_FILE, 'r') as indices_file:
        indices = indices_file.read()

    with open(HEAD_DIR, 'r') as commit_hash:
        prev_commit_hash = commit_hash.read()

    if not indices.strip():
        print("Staging area empty!")
        return
    
    time = datetime.now()
    timestamp = time.strftime("%d/%m/%Y, %H:%M:%S")
    
    commit_obj = f"parent {prev_commit_hash}\n" + f"timestamp {timestamp}\n" + f"message {message}\n" + indices # Save parent hash also to keep track of stuffs
    
    commit_hash = hashlib.sha1(indices.encode()).hexdigest()

    with open(f"{OBJECTS_DIR}/{commit_hash}", "w") as f:
        f.write(commit_obj)

    with open(HEAD_DIR, "w") as f:
        f.write(commit_hash)

    open(INDEX_FILE, "w").close()
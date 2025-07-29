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

    with open(HEAD_DIR, 'r') as head:
        ref = head.read().strip()

    if ref.startswith("ref: "):
        branch_ref = ref[5:] # Format is .mygit/refs/head/<branch_name>
        branch_name = branch_ref.split('/')[-1]
        branch_ref_path = os.path.join(repo_root, ".mygit", branch_ref)

        if os.path.exists(branch_ref_path):
            with open(branch_ref_path, 'r') as commit_hash:
                prev_commit_hash = commit_hash.read().strip()
        else:
            prev_commit_hash = ""
    else: # if head detached due to checking out to a previous commit
        prev_commit_hash = ref
        branch_name = ""  # No branch

    if not indices.strip():
        print("Staging area empty!")
        return
    
    time = datetime.now()
    timestamp = time.strftime("%d/%m/%Y, %H:%M:%S")
    
    # Store branch name in commit object
    commit_obj = (
        f"parent {prev_commit_hash}\n"
        f"timestamp {timestamp}\n"
        f"branch {branch_name}\n"
        f"message {message}\n"
        f"{indices}"
    )
    
    commit_hash = hashlib.sha1(indices.encode()).hexdigest()

    with open(f"{OBJECTS_DIR}/{commit_hash}", "w") as f:
        f.write(commit_obj)

    if ref.startswith("ref: "):
        with open(branch_ref_path, "w") as f:
            f.write(commit_hash)
    else:
        with open(HEAD_DIR, "w") as f:
            f.write(commit_hash)
    
    open(INDEX_FILE, "w").close()
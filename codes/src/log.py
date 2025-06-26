import os
from src.root_finder import get_repo_root

def log():
    repo_root = get_repo_root()
    HEAD = os.path.join(repo_root, ".mygit/HEAD")
    OBJ_DIR = os.path.join(repo_root, ".mygit/objects")

    if not os.path.exists(HEAD):
        print("Warning: No HEAD found.")
        return
    
    with open(HEAD, 'r') as head:
        last_commit_hash = head.read().strip()

    if not last_commit_hash:
        print("No commits to show!")
        return

    while last_commit_hash:
        commit_path = os.path.join(OBJ_DIR, last_commit_hash)

        if not os.path.exists(commit_path):
            print(f"Warning: Commit: {last_commit_hash} not found.")
            break

        with open(commit_path, 'r') as f:
            lines = f.readlines()

        parent = ""
        timestamp = ""
        message = ""

        for line in lines:
            if line.startswith("parent "):
                parent = line[len("parent "):].strip()
            elif line.startswith("timestamp "):
                timestamp = line[len("timestamp "):].strip()
            elif line.startswith("message "):
                message = line[len("message "):].strip()

        print(f" Commit: {last_commit_hash}\n Parent: {parent if parent else "None"}\n Timestamp: {timestamp}\n Message: {message}\n")

        if not parent:
                break

        last_commit_hash = parent
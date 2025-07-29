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
        ref = head.read().strip()

    if ref.startswith("ref: "):
        branch_ref = ref[5:]
        branch_name = branch_ref.split('/')[-1]
        branch_ref_path = os.path.join(repo_root, ".mygit", branch_ref)
        if not os.path.exists(branch_ref_path):
            print(f"Warning: Branch ref {branch_ref} not found.")
            return
        with open(branch_ref_path, 'r') as f:
            last_commit_hash = f.read().strip()
    else:
        branch_name = None
        last_commit_hash = ref

    # Print branch or detached HEAD info at the top
    if branch_name:
        print(f"On branch: {branch_name}\n")
    else:
        print(f"HEAD detached at {last_commit_hash}\n")

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
        commit_branch = ""

        for line in lines:
            if line.startswith("parent "):
                parent = line[len("parent "):].strip()
            elif line.startswith("timestamp "):
                timestamp = line[len("timestamp "):].strip()
            elif line.startswith("branch "):
                commit_branch = line[len("branch "):].strip()
            elif line.startswith("message "):
                message = line[len("message "):].strip()

        # Show branch name from commit object if present
        if commit_branch:
            print(f"[{commit_branch}] Commit: {last_commit_hash}")
        else:
            print(f"Commit: {last_commit_hash}")

        print(f" Parent: {parent if parent else 'None'}")
        print(f" Timestamp: {timestamp}")
        print(f" Message: {message}\n")

        if not parent:
            break

        last_commit_hash = parent
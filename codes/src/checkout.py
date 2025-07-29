import os
from src.root_finder import get_repo_root

def checkout(target):
    repo_root = get_repo_root()
    OBJ_DIR = os.path.join(repo_root, ".mygit/objects")
    HEAD = os.path.join(repo_root, ".mygit/HEAD")
    refs_dir = os.path.join(repo_root, ".mygit/refs/head")
    branch_ref_path = os.path.join(refs_dir, target)

    # Check if the target provided is a branch
    if os.path.exists(branch_ref_path):
        # If it's a branch, update HEAD to point to the branch ref
        with open(branch_ref_path, 'r') as f:
            commit_hash = f.read().strip()
        with open(HEAD, 'w') as f:
            f.write(f"ref: refs/head/{target}")
        print(f"Switched to branch '{target}'")
    else:
        # Assume it's a commit hash and update HEAD to point directly to the commit (detached)
        commit_hash = target
        with open(HEAD, 'w') as f:
            f.write(commit_hash)
        print(f"Checked out to commit {commit_hash} (detached HEAD)")

    # Restore files from the resolved commit
    commit_path = os.path.join(OBJ_DIR, commit_hash)
    if not os.path.exists(commit_path):
        print(f"Error: Commit {commit_hash} not found!")
        return

    with open(commit_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("parent ") or line.startswith("timestamp ") or line.startswith("message ") or line.startswith("branch "):
            continue

        file_path, blob_hash = line.strip().split()
        blob_path = os.path.join(OBJ_DIR, blob_hash)

        if not os.path.exists(blob_path):
            print(f"Error: missing blob object for {file_path}")
            continue

        full_file_path = os.path.join(repo_root, file_path)
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        with open(blob_path, 'rb') as src, open(full_file_path, 'wb') as dst:
            dst.write(src.read())
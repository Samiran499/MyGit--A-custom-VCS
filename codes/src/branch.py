import os
from src.root_finder import get_repo_root

def branch(branch_name, start_point=None):
    repo_root = get_repo_root()
    BRANCHES_DIR = os.path.join(repo_root, ".mygit/refs/head")
    HEAD_DIR = os.path.join(repo_root, ".mygit/HEAD")
    new_branch = os.path.join(BRANCHES_DIR, branch_name)

    if os.path.exists(new_branch):
        print(f"Branch {branch_name} already exists!")
        return

    # Determine the commit to branch from
    if start_point:
        refs_dir = os.path.join(repo_root, ".mygit/refs/head")
        branch_ref_path = os.path.join(refs_dir, start_point)
        if os.path.exists(branch_ref_path):
            with open(branch_ref_path, 'r') as f:
                commit_hash = f.read().strip()
        else:
            # Assume it's a commit hash
            commit_hash = start_point
    else:
        with open(HEAD_DIR, 'r') as head:
            ref = head.read().strip()
        if ref.startswith("ref: "):
            ref_path = os.path.join(repo_root, ".mygit", ref[5:])
            with open(ref_path, 'r') as ref_p:
                commit_hash = ref_p.read().strip()
        else:
            commit_hash = ref  # detached HEAD

    with open(new_branch, 'w') as new_br:
        new_br.write(commit_hash)

    print(f"New branch {branch_name} created at commit {commit_hash}")

def show_branch():
    repo_root = get_repo_root()
    BRANCHES_DIR = os.path.join(repo_root, ".mygit/refs/head")
    HEAD_DIR = os.path.join(repo_root, ".mygit/HEAD")

    with open(HEAD_DIR, 'r') as head:
        ref = head.read().strip()

    current_branch_name = None
    if ref.startswith("ref: "):
        current_branch_name = ref[5:].split('/')[-1]

    branches = os.listdir(BRANCHES_DIR)
    for branch in branches:
        if branch == current_branch_name:
            print(f"* {branch}")
        else:
            print(f"  {branch}")

    if current_branch_name is None:
        print(f"\n(HEAD detached at commit {ref})")
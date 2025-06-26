import os
from src.root_finder import get_repo_root

def status():
    try:
        repo_path = get_repo_root()
        INDEX = os.path.join(repo_path, ".mygit/index")

        if not os.path.exists(INDEX) or os.path.getsize(INDEX) == 0:
            print("Nothing to commit. Staging area is clean.")
            return
        
        print("Files staged for commit:\n")
        with open(INDEX, "r") as f:
            for line in f:
                file_path = line.strip().split()[0]
                print(f' -{file_path}')

    except Exception as e:
        print(f'Error: {e}')
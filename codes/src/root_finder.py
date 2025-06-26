import os

def find_repo_root():
    """Searches upward for the root of the repo essentially to find the .mygit directory, returns the path and None if not found"""
    curr_path = os.getcwd()

    level = 5 # Levels above current directory to keep searching

    while level > 0:
        if os.path.isdir(os.path.join(curr_path, ".mygit")):
            return curr_path
        
        new_path = os.path.dirname(curr_path)
        if new_path == curr_path: # Reached the root directory
            break
        curr_path = new_path

    return None

def get_repo_root():
    repo_root = find_repo_root()
    if not repo_root:
        raise Exception("Not inside a MyGit repository!")
    return repo_root

def normalize_path(input_file): # Normalize absolute path to relative part with respect to root directory of the repo
    repo_root = find_repo_root()
    file_path = os.path.abspath(input_file)

    if not file_path.startswith(repo_root):
        raise Exception("File is outside the repository")
    
    relative_path = file_path[len(repo_root)+1:]
    
    return relative_path
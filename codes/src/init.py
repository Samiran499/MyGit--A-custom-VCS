import os

def init():
    if os.path.exists(".mygit"):
        print("There exists a repository")
        return
    
    os.makedirs(".mygit")
    os.makedirs(".mygit/objects")
    os.makedirs(".mygit/refs")
    os.makedirs(".mygit/refs/head")

    with open(".mygit/index", "w") as index:
        pass
    with open(".mygit/HEAD", "w") as head:
        head.write("ref: refs/head/main")
        
    with open(".mygit/refs/head/main", "w") as main:
        pass

    print("MyGit repo initialized!")
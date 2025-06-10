import os

def init():
    if os.path.exists(".mygit"):
        print("There exists a repository")
        return
    
    os.makedirs(".mygit")
    os.makedirs(".mygit/objects")
    os.makedirs(".mygit/refs")

    with open(".mygit/index", "w") as index:
        pass
    with open(".mygit/HEAD", "w") as head:
        pass

    print("MyGit repo initialized!")
import argparse
from src.init import init
from src.add import add

def commit(message):
    print(f"Committed with message: '{message}'")

def status():
    print("Status: No changes to commit.")

def log():
    print("Showing commit history...")

def main():
    parser = argparse.ArgumentParser(description="MyGit- A simple VCS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # init
    subparsers.add_parser("init", help="Initialize repository")

    # add
    parser_add = subparsers.add_parser("add", help="Add files to staging")
    parser_add.add_argument("files", nargs="+", help="Files to add")

    # commit
    parser_commit = subparsers.add_parser("commit", help="Commit changes")
    parser_commit.add_argument("-m", "--message", help="Commit message")

    # status
    subparsers.add_parser("status", help="Show repo status")

    # log
    subparsers.add_parser("log", help="Show commit history")

    args = parser.parse_args()

    # Command dispatch
    if args.command == "init":
        init()
    elif args.command == "add":
        add(args.files)
    elif args.command == "commit":
        commit(args.message)
    elif args.command == "status":
        status()
    elif args.command == "log":
        log()

if __name__ == "__main__":
    main()
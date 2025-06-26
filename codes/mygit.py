import argparse
from src.init import init
from src.add import add
from src.commit import commit
from src.status import status
from src.log import log
from src.checkout import checkout

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

    # checkout
    parser_checkout = subparsers.add_parser("checkout", help="Checkout to an old commit")
    parser_checkout.add_argument("commit_hash", help="Hash of an old commit")

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
    elif args.command == "checkout":
        checkout(args.commit_hash)

if __name__ == "__main__":
    main()
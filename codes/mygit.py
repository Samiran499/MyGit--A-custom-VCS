#!/usr/bin/env python3

import argparse
import os
from src.init import init
from src.add import add
from src.commit import commit
from src.status import status
from src.log import log
from src.checkout import checkout
from src.branch import branch, show_branch
from src.root_finder import get_repo_root

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
    parser_checkout = subparsers.add_parser("checkout", help="Checkout to a branch or commit")
    parser_checkout.add_argument("target", nargs="?", help="Branch name or commit hash")
    parser_checkout.add_argument("-b", "--branch", help="Create a new branch and checkout to it")

    # branch
    parser_branch = subparsers.add_parser("branch", help="Create a new branch")
    parser_branch.add_argument("branch_name", nargs="?", help="Name of the new branch")

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
        if args.branch:
            # Check if branch already exists before creating
            repo_root = get_repo_root()
            branch_path = os.path.join(repo_root, ".mygit/refs/head", args.branch)
            if not os.path.exists(branch_path):
                branch(args.branch, start_point=args.target)
            checkout(args.branch)
        else:
            checkout(args.target)
    elif args.command == "branch":
        if not args.branch_name:
            show_branch()
        else:
            branch(args.branch_name)

if __name__ == "__main__":
    main()
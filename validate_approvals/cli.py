import argparse
from argparse import ArgumentParser
from typing import Generator

from validate_approvals.core import Validator


def create_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--approvers", type=str)
    parser.add_argument("--changed-files", type=str)

    return parser


def get_split_arguments(arg: str) -> Generator[str, None, None]:
    return (value.strip() for value in arg.split(","))


def run(args, repo_root="") -> str:
    approvers = changed_files = None
    if args.approvers:
        approvers = list(get_split_arguments(args.approvers))
    if args.changed_files:
        changed_files = list(get_split_arguments(args.changed_files))

    if approvers and changed_files:
        validator = Validator(
            repo_root=repo_root, changed_files=changed_files, approvers=approvers
        )
        return validator.validate()
    else:
        return "Both --approvers and --changed-files must be set!\n"


def main():
    parser = create_parser()
    print(run(parser.parse_args()))

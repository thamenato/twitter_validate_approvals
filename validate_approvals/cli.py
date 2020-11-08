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


def run() -> str:
    parser = create_parser()
    args = parser.parse_args()

    approvers = changed_files = None
    if args.approvers:
        approvers = tuple(get_split_arguments(args.approvers))
    if args.changed_files:
        changed_files = tuple(get_split_arguments(args.changed_files))

    validator = Validator(changed_files=changed_files, approvers=approvers)
    return validator.validate()


if __name__ == "__main__":
    run()

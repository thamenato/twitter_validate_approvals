import argparse


def create_parser():
    parser = argparse.ArgumentParser(description="")

    parser.add_argument("--approvers", type=str)
    parser.add_argument("--changed-files", type=str)

    return parser


def get_split_argument_list(arg: str):
    return [value.strip() for value in arg.split(",")]


def run():
    parser = create_parser()
    args = parser.parse_args()

    approvers = changed_files = None
    if args.approvers:
        approvers = get_split_argument_list(args.approvers)
    if args.changed_files:
        changed_files = get_split_argument_list(args.changed_files)

    print(approvers)
    print(changed_files)


if __name__ == "__main__":
    run()

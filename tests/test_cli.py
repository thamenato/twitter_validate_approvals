import pytest
from validate_approvals.cli import create_parser, get_split_argument_list


class TestCLI:
    @pytest.fixture()
    def parser(self):
        return create_parser()

    def test_argument_parser(self, parser):
        args = parser.parse_args([])
        assert args

        args = parser.parse_args(["--approvers", "johndoe"])
        assert args.approvers

        args = parser.parse_args(["--changed-files", "folder/goes/here"])
        assert args.changed_files

    def test_get_split_argument_list(self, parser):
        approvers = ["lovelace", "turing", "johndoe"]

        for i in range(0, len(approvers)):
            expected_values = approvers[i:]
            test_cases = (
                ",".join(expected_values),
                ", ".join(expected_values),
                " ,".join(expected_values),
                " , ".join(expected_values),
            )

            for case in test_cases:
                args = parser.parse_args(["--approvers", case])
                assert get_split_argument_list(args.approvers) == expected_values

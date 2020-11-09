from typing import List, Tuple

import pytest

from validate_approvals.cli import create_parser, get_split_arguments, run


def _get_approvers_str_arguments() -> List[Tuple[str, Tuple[str, ...]]]:
    """Return permutation of approvers and whitespaces with semicolons

    Returns:
        List[Tuple[str, Tuple[str]]]: List containing all test cases to be used
            with pytest parametrization.
    """

    approvers = ("lovelace", "turing", "johndoe")
    test_cases = (",", ", ", " ,", " , ")

    str_arguments = []
    for i in range(0, len(approvers) - 1):
        expected_value = approvers[i:]

        for case in test_cases:
            cmd_line_arg = case.join(expected_value)
            str_arguments.append((cmd_line_arg, expected_value))

    str_arguments.append((approvers[-1], approvers[-1:]))

    return str_arguments


class TestCLI:
    @pytest.fixture(scope="class")
    def repo_root(self):
        return

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

    @pytest.mark.parametrize("argument, expected_value", _get_approvers_str_arguments())
    def test_get_split_arguments(self, parser, argument, expected_value):
        args = parser.parse_args(["--approvers", argument])
        assert tuple(get_split_arguments(args.approvers)) == expected_value

    @pytest.mark.parametrize(
        "approvers, changed_files, expected_result",
        [
            (
                "alovelace,ghopper,eclarke",  # missing eclarke or kantonelli from example
                "tests/repo_root/src/com/twitter/follow/Follow.java,tests/repo_root/src/com/twitter/user/User.java",
                "Approved",
            ),
            (
                "alovelace",
                "tests/repo_root/src/com/twitter/follow/Follow.java",
                "Insufficient approvals",
            ),
            (
                "eclarke",
                "tests/repo_root/src/com/twitter/follow/Follow.java",
                "Insufficient approvals",
            ),
            (
                "alovelace,eclarke",
                "tests/repo_root/src/com/twitter/follow/Follow.java",
                "Approved",
            ),
            ("mfox", "tests/repo_root/src/com/twitter/tweet/Tweet.java", "Approved"),
        ],
    )
    def test_repo_root(self, parser, approvers, changed_files, expected_result):
        args = parser.parse_args(
            ["--approvers", approvers, "--changed-files", changed_files]
        )
        assert run(args, "tests/repo_root") == expected_result

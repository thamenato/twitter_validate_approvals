from typing import List, Tuple

import pytest

from tests import TWITTER_SRC
from validate_approvals.dependencies import get_dependencies


def changed_files() -> List[Tuple[str, List[str]]]:
    return [
        (f"{TWITTER_SRC}/follow/Follow.java", ["src/com/twitter/user"]),
        (
            f"{TWITTER_SRC}/message/Message.java",
            ["src/com/twitter/follow", "src/com/twitter/user"],
        ),
        (f"{TWITTER_SRC}/user/User.java", []),
    ]


class TestDependencies:
    @pytest.mark.parametrize(("changed_file", "expected_value"), changed_files())
    def test_get_dependencies(self, changed_file, expected_value):
        assert get_dependencies(changed_file) == expected_value

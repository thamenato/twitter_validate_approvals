import pytest

from tests import TWITTER_SRC
from validate_approvals.core import get_dependencies, get_owners


@pytest.mark.parametrize(
    "changed_file, expected_value",
    [
        (f"{TWITTER_SRC}/follow/Follow.java", ["src/com/twitter/user"]),
        (
            f"{TWITTER_SRC}/message/Message.java",
            ["src/com/twitter/follow", "src/com/twitter/user"],
        ),
        (f"{TWITTER_SRC}/user/User.java", []),
    ],
)
def test_get_dependencies(changed_file, expected_value):
    assert get_dependencies(changed_file) == expected_value


@pytest.mark.parametrize(
    "changed_file, expected_value",
    [
        (f"{TWITTER_SRC}/follow/Follow.java", ["alovelace", "ghopper"]),
        (f"{TWITTER_SRC}/user/User.java", ["ghopper"]),
    ],
)
def test_get_owners(changed_file, expected_value):
    assert get_owners(changed_file) == expected_value

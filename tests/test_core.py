import pytest

from tests import TWITTER_SRC
from validate_approvals.core import get_owners, get_transitive_dependencies


@pytest.mark.parametrize(
    "changed_file, expected_value",
    [
        (f"{TWITTER_SRC}/follow/Follow.java", ["alovelace", "ghopper"]),
        (f"{TWITTER_SRC}/user/User.java", ["ghopper"]),
    ],
)
def test_get_owners(changed_file, expected_value):
    assert get_owners(changed_file) == expected_value


def test_get_transitive_dependencies(fake_repo):
    transitive_deps = get_transitive_dependencies(str(fake_repo.realpath()))
    assert transitive_deps.get("y") == {"x", "z"}

import pytest

from tests import TWITTER_SRC
from validate_approvals.utils import get_path


def test_get_path():
    assert get_path(f"{TWITTER_SRC}/tweet/Tweet.java", "DEPENDENCIES").exists()


def test_get_path_invalid_file():
    with pytest.raises(ValueError):
        get_path("lorem/ipsum.dolor", "")

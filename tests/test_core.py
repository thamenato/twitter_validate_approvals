import pytest

from tests import TWITTER_SRC
from validate_approvals.core import Validator


class TestValidator:
    @pytest.fixture
    def validator(self, fake_repo):
        return Validator(
            repo_root=str(fake_repo.realpath()), changed_files="", approvers=""
        )

    @pytest.mark.parametrize(
        "changed_file, expected_value",
        [
            (f"{TWITTER_SRC}/follow", ["alovelace", "ghopper"]),
            (f"{TWITTER_SRC}/user", ["ghopper"]),
        ],
    )
    def test_get_folder_owners(self, validator, changed_file, expected_value):
        assert validator._get_folder_owners(changed_file) == expected_value

    def test_get_transitive_dependencies(self, validator):
        assert validator.transitive_dependencies.get("x") == {"z"}
        assert validator.transitive_dependencies.get("y") == {"x", "z"}
        assert validator.transitive_dependencies.get("z") is None

    def test_set_all_owners(self, fake_repo, validator):
        repo_root = str(fake_repo.realpath())
        validator.changed_files = [f"{repo_root}/y/file"]
        validator._set_all_owners()
        assert validator.owners == {"y": ["B", "C"]}

    def test_validate(self, validator):
        result = validator.validate()
        assert result == "Approved"

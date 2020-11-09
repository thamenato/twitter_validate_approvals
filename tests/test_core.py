import pytest

from validate_approvals.core import Validator


class TestValidator:
    @pytest.mark.parametrize(
        "changed_file, expected_value",
        [("x", ["A", "B"]), ("y", ["B", "C"]), ("z", ["D"])],
    )
    def test_get_folder_owners(self, fake_repo, changed_file, expected_value):
        repo_root = str(fake_repo.realpath())
        validator = Validator(repo_root=repo_root)
        assert (
            validator._get_folder_owners(f"{repo_root}/{changed_file}")
            == expected_value
        )

    def test_get_transitive_dependencies(self, fake_repo):
        validator = Validator(repo_root=str(fake_repo.realpath()))
        assert validator.transitive_dependencies.get("x") == {"z"}
        assert validator.transitive_dependencies.get("y") == {"x", "z"}
        assert validator.transitive_dependencies.get("z") is None

    @pytest.mark.parametrize(
        "changed_files, expected_value",
        [
            (["y/file"], {"y": ["B", "C"], "x": ["A", "B"], "z": ["D"]}),
            (["z/a.txt", "x/b.txt"], {"x": ["A", "B"], "z": ["D"]}),
            (["z/a.txt"], {"z": ["D"]}),
        ],
    )
    def test_set_all_owners(self, fake_repo, changed_files, expected_value):
        repo_root = str(fake_repo.realpath())
        validator = Validator(
            repo_root=repo_root,
            changed_files=[f"{repo_root}/{name}" for name in changed_files],
        )
        validator._set_all_owners()
        assert validator.owners == expected_value

    @pytest.mark.parametrize(
        "changed_files, approvers, expected_value",
        [
            (["y/file"], ["A", "C", "D"], Validator._APPROVED),
            (["y/file"], ["B", "D"], Validator._APPROVED),
            (["y/file"], ["A"], Validator._NOT_APPROVED),
            (["z/a.txt"], ["D"], Validator._APPROVED),
            (["x/b.txt"], ["D"], Validator._NOT_APPROVED),
            (["x/b.txt"], ["A", "B", "D"], Validator._APPROVED),
        ],
    )
    def test_validate(self, fake_repo, changed_files, approvers, expected_value):
        repo_root = str(fake_repo.realpath())
        validator = Validator(
            repo_root=repo_root,
            changed_files=[f"{repo_root}/{name}" for name in changed_files],
            approvers=approvers,
        )
        result = validator.validate()
        assert result == expected_value

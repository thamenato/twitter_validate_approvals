from pathlib import Path

from validate_approvals.utils import get_file_content, get_folder_path, get_folders


def test_get_folders(fake_repo):
    repo_root = str(fake_repo.realpath())
    folders = [f"{repo_root}/y/file"]
    assert get_folders(folders) == [f"{repo_root}/y"]


def test_get_folder_path(fake_repo):
    path = Path(f"{fake_repo.realpath()}/y/file")
    folder = get_folder_path(path)

    assert folder.is_dir()
    assert str(folder) == f"{fake_repo.realpath()}/y"


def test_get_file_content(fake_repo):
    path = Path(f"{fake_repo.realpath()}/x/OWNERS")
    content = get_file_content(path)
    assert content == ["A", "B"]


def test_get_file_content_invalid_path():
    path = Path("lorem/ipsum.dolor")
    content = get_file_content(path)
    assert content == []

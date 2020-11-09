from pathlib import Path
from typing import List


def get_folders(changed_files: List[str]) -> List[str]:
    return [str(get_folder_path(folder)) for folder in changed_files]


def get_folder_path(changed_file: str) -> Path:
    path = Path(changed_file)
    if not path.exists():
        raise ValueError(f"file {changed_file} does not exists")

    return path.parent


def get_file_content(path: Path) -> List[str]:
    if path.exists():
        with path.open("r") as fp:
            return [line.strip() for line in fp.readlines()]
    return []

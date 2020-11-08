from pathlib import Path
from typing import List


def get_path(changed_file: str, desired_file: str) -> Path:
    if not Path(changed_file).resolve().exists():
        raise ValueError(f"file {changed_file} does not exists")

    return Path(changed_file).parent.joinpath(desired_file)


def get_file_content(path: Path) -> List[str]:
    if path.exists():
        with path.open("r") as fp:
            return [line.strip() for line in fp.readlines()]
    return []

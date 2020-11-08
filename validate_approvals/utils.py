from pathlib import Path


def get_path(changed_file: str, desired_file: str) -> Path:
    if not Path(changed_file).resolve().exists():
        raise ValueError(f"file {changed_file} does not exists")

    return Path(changed_file).parent.joinpath(desired_file)

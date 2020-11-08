from typing import List

from validate_approvals.utils import get_file_content, get_path


def get_dependencies(changed_file: str) -> List[str]:
    """Try to read from DEPENDENCIES file at the changed_file folder.

    Args:
        changed_file (str): path for the file that changed.

    Returns:
        List[str]: List containing the file path for all dependencies.
    """
    path = get_path(changed_file, "DEPENDENCIES")
    return get_file_content(path)


def get_owners(changed_file: str) -> List[str]:
    """Return the owners for the file that changed.

    If at the folder of the changed file does not have an OWNERS file
    it will look at the parent folder recursively until it finds one.

    Args:
        changed_file (str): path for the file that changed.

    Returns:
        List[str]: List containing the name of the owners of those files.
    """
    path = get_path(changed_file, "OWNERS")
    return get_file_content(path) or get_owners(str(path.parent))

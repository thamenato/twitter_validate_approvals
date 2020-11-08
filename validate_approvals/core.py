from glob import glob
from pathlib import Path
from typing import List

from validate_approvals.utils import get_file_content, get_path


def get_transitive_dependencies(repo_root=""):
    repo_root += "/" if repo_root[-1] != "/" else ""
    transitive_deps = {}

    dep_files = glob(f"{repo_root}**/DEPENDENCIES", recursive=True)
    for filepath in dep_files:
        path = Path(filepath)
        curr_folder = str(path.parent).replace(repo_root, "")
        for dependency_folder in get_file_content(path):
            dependencies = transitive_deps.get(dependency_folder, set())
            dependencies.add(curr_folder)
            transitive_deps[dependency_folder] = dependencies

    return transitive_deps


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

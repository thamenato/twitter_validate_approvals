from glob import glob
from pathlib import Path
from typing import Dict, List

from validate_approvals.utils import get_file_content, get_folders


class Validator:
    _APPROVED = "Approved"
    _NOT_APPROVED = "Insufficient approvals"

    def __init__(self, *args, **kwargs) -> None:
        repo_root = kwargs.get("repo_root")
        if repo_root:
            repo_root += "/" if repo_root[-1] != "/" else ""
            self.repo_root = repo_root
        else:
            self.repo_root = ""

        self.transitive_dependencies: Dict[str, List[str]] = {}
        self.owners: Dict[str, List[str]] = {}
        self.changed_files = kwargs.get("changed_files", [])
        self.approvers = kwargs.get("approvers")
        self._set_transitive_dependencies()

    def _set_transitive_dependencies(self):
        """Creates a dict that returns which folders(value) depends on folder(key)

        Seeks for all `DEPENDENCIES` files and read them. For each dependency it
        will add the current folder (where the `DEPENDENCIES` is being read from)
        to a list that represents the transitive dependency.
        """
        dep_files = glob(f"{self.repo_root}**/DEPENDENCIES", recursive=True)
        for filepath in dep_files:
            path = Path(filepath)
            curr_folder = str(path.parent).replace(self.repo_root, "")
            for dependency_folder in get_file_content(path):
                dependencies = self.transitive_dependencies.get(
                    dependency_folder, set()
                )
                dependencies.add(curr_folder)
                self.transitive_dependencies[dependency_folder] = dependencies

    def _set_all_owners(self):
        """Define all the owners for changed files and transitive dependencies

        Get the owners for the folders where the changed files belongs to,
        then verify for transitive dependencies and get the owners for
        them too.
        """
        direct_dependency = get_folders(self.changed_files)
        all_folders = set(direct_dependency)
        for folder in direct_dependency:
            folder_name = folder.replace(self.repo_root, "")
            dependencies = [
                f"{self.repo_root}{f}"
                for f in self.transitive_dependencies.get(folder_name, [])
            ]
            all_folders = all_folders.union(set(dependencies))

        for folder in all_folders:
            folder_name = folder.replace(self.repo_root, "")
            self.owners[folder_name] = self._get_folder_owners(folder)

    def _get_folder_owners(self, filepath: str) -> List[str]:
        """Return the owners for the file that changed.

        If at the folder of the changed file does not have an OWNERS file
        it will look at the parent folder recursively until it finds one.

        Args:
            changed_file (str): path for the file that changed.

        Returns:
            List[str]: List containing the name of the owners of those files.
        """
        path = Path(filepath)
        if str(self.repo_root[:-1]) in str(path.resolve()):
            # only runs if it's a child of repo_root
            owners = get_file_content(path.joinpath("OWNERS"))
            return owners or self._get_folder_owners(str(path.parent))
        return []

    def validate(self) -> str:
        self._set_all_owners()
        for owners in self.owners.values():
            if not set(self.approvers).intersection(set(owners)):
                return self._NOT_APPROVED
        return self._APPROVED

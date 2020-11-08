from glob import glob
from pathlib import Path
from typing import Dict, List

from validate_approvals.utils import get_file_content, get_folders


class Validator:
    owners: Dict[str, List[str]] = {}
    transitive_dependencies: Dict[str, List[str]] = {}
    repo_root: str = ""

    def __init__(self, *args, **kwargs) -> None:
        repo_root = kwargs.get("repo_root")
        if repo_root:
            repo_root += "/" if repo_root[-1] != "/" else ""
            self.repo_root = repo_root

        self._set_transitive_dependencies()
        self.changed_files = kwargs["changed_files"]
        self.approvers = kwargs["approvers"]

    def _set_transitive_dependencies(self):
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
        folder_list = get_folders(self.changed_files)
        for folder in folder_list:
            folder_owners = self._get_folder_owners(folder)
            self.owners[folder.replace(self.repo_root, "")] = folder_owners

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
        owners = get_file_content(path.joinpath("OWNERS"))
        return owners or self._get_folder_owners(str(path.parent))

    def validate(self) -> str:
        self._set_all_owners()

        return "Approved"

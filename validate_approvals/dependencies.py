from validate_approvals.utils import get_path


def get_dependencies(changed_file: str):
    path = get_path(changed_file, "DEPENDENCIES")

    if path.exists():
        with path.open("r") as fp:
            return [dep.strip() for dep in fp.readlines()]
    else:
        return []

import pytest


@pytest.fixture(scope="session")
def fake_repo(tmpdir_factory):
    # create root and an OWNERS file
    root = tmpdir_factory.mktemp("fake_repo")
    fp = root.join("OWNERS")
    fp.write("D\n")

    # create the rest of the repo inside the root
    repo = {
        "x": [("DEPENDENCIES", "y\n"), ("OWNERS", "A\nB\n"), ("b.txt", "")],
        "y": [("OWNERS", "B\nC\n"), ("file", "")],
        "z": [("DEPENDENCIES", "y\nx\n"), ("a.txt", "")],
    }
    for folder_name, file_list in repo.items():
        folder_fp = root.mkdir(folder_name)
        for file_name, content in file_list:
            fp = folder_fp.join(file_name)
            fp.write(content)

    return root

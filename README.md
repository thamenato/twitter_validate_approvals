# Validate Approvals

Challenge description [here](resources/CHALLENGE.md).


## Installing Dependencies

_Note: This project uses [poetry](https://python-poetry.org) as it's dependency manager so make sure that_
_you have latest `poetry` installed locally._

To create the virtual environment, install and dependencies and the
`validate_approvals` CLI, simply run:

```shell
$ poetry install
```

Once that's done you can either run all commands by using the `poetry run <command>`
or opening a shell session with the virtual env loaded: `poetry shell`

If `poetry` can't be used a `requirements.txt` file containing all dependencies
including development ones is also present to allow using `pip`.


## Testing

All the tests are under the `tests` folder and they can be run using

```shell
$ poetry run pytest
```


## Running the CLI directly

If using `poetry` you can access a new shell with the virtual environment
`poetry shell` and run it directly with:

```shell
$ validate_approvals -h

$ validate_approvals --approvers johndoe \
    --changed-files src/python/cool_lib/somefile.py
```

# Bobabot

## Getting started

Fork and clone

```shell
cd bobabot
```

Navigate into project

```shell
python -m venv venv
```

Initialize your python virtual environment

_note: This is only necessary for new environment setups_

```shell
source venv/bin/activate
```

Activate the python virtual environment

```shell
pip install -r requirements.txt
pip install -r requirements.dev.txt
```

Install project dependencies into virtual environment

### Linting

This project uses [Black](https://github.com/psf/black) as formatting guidelines. [Pre-commit](https://pre-commit.com/) is used to auto format as users commit their work.

```shell
pre-commit run --all-files
```

Run pre-commit on all files to check current formatting status of the project.

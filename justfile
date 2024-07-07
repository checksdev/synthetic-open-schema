poetry-install:
    poetry -C src install

pre-commit-install:
    poetry -C src run -- pre-commit install

install: poetry-install pre-commit-install

pre-commit:
    poetry -C src run -- pre-commit run --all-files -v

test:
    poetry -C src run -- ptw --ext=.py,.yml,.yaml,.ini examples src

ci-test:
    cd src && poetry run -- pytest

dump:
    poetry -C src run -- python scripts/dump_schemas.py > schemas/v1beta1.json

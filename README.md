# lol_qq_parser

A League of Legends parser for QQ data

## Sources

This package relies on the API used by [lpl.qq.com](https://lpl.qq.com/).
Unofficial Chinese documentation can be [found here](https://documenter.getpostman.com/view/3922302/UVCCfjUk).

## Examples

```python
# TODO
```

## Development

### Environment setup

Install dependencies in a virtual environment with `poetry`:

```shell
poetry install
```

### Running tests

Run tests through `pytest`. They should be found automatically in VS Code.

```shell
poetry run pytest .
```

### Generating schemas

The `/data/create_schemas.py` file generates `pydantic` validation schemas.

It can be run as a task in VS Code with the `Run Task` command, or from the terminal with `poetry run python data/create_schemas.py`

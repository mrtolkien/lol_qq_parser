# lol_qq_parser

A League of Legends parser for QQ data

## Sources

This package relies on the API used by [lpl.qq.com](https://lpl.qq.com/).
Unofficial Chinese documentation can be [found here](https://documenter.getpostman.com/view/3922302/UVCCfjUk).

## Examples

```python
import lol_qq_parser

# Get a series by its ID
# Example URL: https://lpl.qq.com/es/stats.shtml?bmid=8108
series = lol_qq_parser.get_series_basic_info(8108)
```

## Development

As shown [here](https://documenter.getpostman.com/view/3922302/UVCCfjUk), there are many more endpoints that are not implemented in this package.

Any help is welcome to support all known endpoints!

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

The `/data/create_schemas.py` file generates `pydantic` validation schemas for QQ endpoints.

It can be run as a task in VS Code with the `Run Task` command, or from the terminal with `poetry run python data/create_schemas.py`

If you add new endpoints to the package, please add data validation to them for easier maintenance.

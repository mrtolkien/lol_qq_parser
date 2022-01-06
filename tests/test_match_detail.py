import os
import pytest
import json

match_id_list = [8108, 8269]


@pytest.mark.parametrize("match_id", match_id_list)
def test_get_match_raw(request, match_id):
    """
    Tests the endpoint called matchDetail and dumps the raw JSON
    """
    from lol_qq_parser.parsers.match_detail import get_match_detail_raw

    raw_dump_folder = os.path.join("data", "matchDetail")
    os.makedirs(raw_dump_folder, exist_ok=True)

    match_detail_raw = get_match_detail_raw(match_id)

    assert match_detail_raw["success"]

    raw_dump_file = os.path.join(raw_dump_folder, f"{match_id}.json")

    with open(raw_dump_file, "w+") as file:
        json.dump(match_detail_raw, file)

    # Using the pytest cache to pass data from test to test in this file
    request.config.cache.set(f"{match_id}_raw", match_detail_raw)


@pytest.mark.parametrize("match_id", match_id_list)
def test_validate_match(request, match_id):
    import lol_qq_parser.schemas.match_detail

    # Getting the raw match details
    match_detail_raw = request.config.cache.get(f"{match_id}_raw", None)

    assert match_detail_raw

    match_detail = lol_qq_parser.schemas.match_detail.Model(**match_detail_raw)

    # This validates that matchId was properly cast to an integer
    assert match_detail.data.matchId == match_id

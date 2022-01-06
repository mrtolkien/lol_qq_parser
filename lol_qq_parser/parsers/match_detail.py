import lol_qq_parser.utils
import lol_qq_parser.schemas.match_detail


def get_series_basic_info(match_id: int):
    """
    This takes a matchId (tjstats) or bmid (qq.com) and returns basic information about
    all games in the series
    """
    # Querying tjstats for the raw information
    match_detail_raw = get_match_detail_raw(match_id)

    # Validating that it conforms to our schema
    match_detail = lol_qq_parser.schemas.match_detail.Model(**match_detail_raw)


def get_match_detail_raw(match_id: int) -> dict:
    """
    This returns the raw match detail endpoint data
    """
    match_detail_url = lol_qq_parser.utils.Endpoints.get_match_detail_url(match_id)

    return lol_qq_parser.utils.query_tjstats(match_detail_url)

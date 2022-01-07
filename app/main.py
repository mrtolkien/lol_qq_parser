from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import lol_qq_parser

app = FastAPI(
    title="LoL QQ simplified API",
    description="An API dedicated to retrieving League of Legends data from QQ.com",
    version="0.1",
    contact={"name": "Gary 'Tolki' Mialaret", "email": "gary@statespacelabs.com"},
    default_response_class=ORJSONResponse,
)


@app.get("/series")
def get_series(match_id: int):
    # TODO This does not return sources becaues of my godawful data format
    return lol_qq_parser.get_series_basic_info(match_id=match_id)

from fastapi import FastAPI
import lol_qq_parser

app = FastAPI(
    title="LoL QQ simplified API",
    description="An API dedicated to retrieving League of Legends data from QQ.com",
    version="0.1",
    contact={"name": "Gary 'Tolki' Mialaret", "email": "gary@statespacelabs.com"},
)


@app.get("/series")
def get_series(match_id: int):
    return lol_qq_parser.get_series_basic_info(match_id=match_id)

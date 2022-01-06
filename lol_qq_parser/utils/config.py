# We use a hard-coded config object as values are hard-coded...
class Config:
    # Authorization key seems to be hardcoded, ideally should be dynamic
    headers = {"Authorization": "7935be4c41d8760a28c05581a7b1f570"}
    root_url = "https://open.tjstats.com/match-auth-app/open/"


class Endpoints:
    schedule = "v1/schedule/season?iOpen=-1"

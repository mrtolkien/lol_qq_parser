from lol_dto.classes.game import (
    LolGame,
    LolGameTeam,
    LolGameTeamEndOfGameStats,
    LolGamePlayer,
    LolGamePlayerEndOfGameStats,
    LolGamePlayerItem,
    LolGamePlayerRune,
    LolGamePlayerSummonerSpell,
)
import lol_qq_parser.utils
import lol_qq_parser.schemas.match_detail

from lol_qq_parser.utils import series_dto

# I'm not satisfied with the above imports structure, still kinda struggling with VScode organization


def get_series_basic_info(match_id: int) -> series_dto.LolQQSeries:
    """
    This takes a matchId (tjstats) or bmid (qq.com) and returns basic information about
    all games in the series
    """
    # Querying tjstats for the raw information
    match_detail_raw = get_match_detail_raw(match_id)

    # Validating that it conforms to our schema, pydantic raises on errors
    match_detail = lol_qq_parser.schemas.match_detail.Model(**match_detail_raw)

    # Casting it to a LolSeries
    series = match_detail_to_lol_series(match_detail)

    return series


def get_match_detail_raw(match_id: int) -> dict:
    """
    This returns the raw match detail endpoint data
    """
    match_detail_url = lol_qq_parser.utils.Endpoints.get_match_detail_url(match_id)

    return lol_qq_parser.utils.query_tjstats(match_detail_url)


def match_detail_to_lol_series(
    match_detail: lol_qq_parser.schemas.match_detail.Model,
) -> series_dto.LolQQSeries:

    # We get the winner's name and create a readable score
    if match_detail.data.matchWin == match_detail.data.teamAId:
        series_winner = match_detail.data.teamAName
    elif match_detail.data.matchWin == match_detail.data.teamBId:
        series_winner = match_detail.data.teamBName
    else:
        raise ValueError("Series winner could not be found in the participating teams")

    series_score = {
        match_detail.data.teamAName: match_detail.data.teamAScore,
        match_detail.data.teamBName: match_detail.data.teamBScore,
    }

    # We set the series object without the games first
    lol_series = series_dto.LolQQSeries(
        winner=series_winner,
        score=series_score,
    )

    # This is a very disgusting way to add extra information and the whole DTO should change...
    # But it creates series.sources.qq.matchId as well as basic teams information
    setattr(
        lol_series.sources,
        lol_qq_parser.utils.Config.source_prefix,
        series_dto.LolQQSeriesSource(
            matchId=match_detail.data.matchId,
            teams=[
                series_dto.LolQQTeamSource(
                    id=getattr(match_detail.data, f"team{team_tag}Id"),
                    tag=getattr(match_detail.data, f"team{team_tag}Name"),
                )
                for team_tag in ("A", "B")
            ],
        ),
    )

    for game_info in match_detail.data.matchInfos:
        lol_game = LolGame(
            duration=game_info.gameTime,
            gameInSeries=game_info.bo - 1,
            start=game_info.matchStartTime,
            winner="BLUE" if game_info.matchWin == game_info.blueTeam else "RED",
        )

        for team_info in game_info.teamInfos:
            # We create the basic lol_team skeleton
            lol_team = LolGameTeam(
                bans=team_info.banHeroList,
                endOfGameStats=LolGameTeamEndOfGameStats(
                    baronKills=team_info.baronAmount,
                    # TODO Save information from baronIncome field
                    dragonKills=team_info.dragonAmount,
                    inhibitorKills=team_info.inhibitKills,
                    firstInhibitor=team_info.isFirstInhibitor,
                    firstRiftHerald=team_info.isFirstRiftHerald,
                    firstTurret=team_info.isFirstTurret,
                    turretKills=team_info.turretAmount,
                ),
            )

            setattr(
                lol_team.sources,
                lol_qq_parser.utils.Config.source_prefix,
                series_dto.LolQQTeamSource(
                    id=team_info.teamId,
                    tag=match_detail.data.teamAName
                    if team_info.teamId == match_detail.data.teamAId
                    else match_detail.data.teamBName,
                ),
            )

            # We iterate on the players
            for player_info in team_info.playerInfos:
                lol_player = LolGamePlayer(
                    championId=player_info.heroId,
                    endOfGameStats=LolGamePlayerEndOfGameStats(
                        totalDamageTaken=player_info.DamageTakenDetail.damageTaken,
                        magicDamageTaken=player_info.DamageTakenDetail.magicalDamageTaken,
                        physicalDamageTaken=player_info.DamageTakenDetail.physicalDamageTaken,
                        totalHeal=player_info.DamageTakenDetail.restoreLife,
                        assists=player_info.battleDetail.assist,
                        deaths=player_info.battleDetail.death,
                        # TODO Not entirely sure of that one, maybe it's highestMultiKill?
                        largestKillingSpree=player_info.battleDetail.highestKillStreak,
                        kills=player_info.battleDetail.kills,
                        totalDamageDealtToChampions=player_info.damageDetail.heroDamage,
                        magicDamageDealtToChampions=player_info.damageDetail.heroMagicalDamage,
                        physicalDamageDealtToChampions=player_info.damageDetail.heroPhysicalDamage,
                        largestCriticalStrike=player_info.damageDetail.highestCritDamage,
                        totalDamageDealt=player_info.damageDetail.totalDamage,
                        magicDamageDealt=player_info.damageDetail.totalMagicalDamage,
                        physicalDamageDealt=player_info.damageDetail.totalPhysicalDamage,
                        items=[
                            LolGamePlayerItem(id=item_info.itemId)
                            for item_info in player_info.items
                        ]
                        + [LolGamePlayerItem(id=player_info.trinketItem.itemId)],
                        # Despite it being called minionKilled, it's the creep score and includes monsters
                        cs=player_info.minionKilled,
                        monsterKills=player_info.otherDetail.totalNeutralMinKilled,
                        firstBlood=player_info.otherDetail.firstBlood,
                        # There's also a field called firstTurret, not sure what the difference is...
                        firstTurret=player_info.otherDetail.firstTurretKill,
                        firstTurretAssist=player_info.otherDetail.firstTurretAssist,
                        gold=player_info.otherDetail.golds,
                        goldSpent=player_info.otherDetail.spentGold,
                        level=player_info.otherDetail.level,
                        monsterKillsInEnemyJungle=player_info.otherDetail.totalMinKilledEnemyJungle,
                        monsterKillsInAlliedJungle=player_info.otherDetail.totalMinKilledYourJungle,
                        turretKills=player_info.otherDetail.turretAmount,
                        visionScore=player_info.visionDetail.visionScore,
                        wardsPlaced=player_info.visionDetail.wardPlaced,
                        wardsKilled=player_info.visionDetail.wardKilled,
                        visionWardsBought=player_info.visionDetail.controlWardPurchased,

                        # technically this is wrong, a player COULD get 2 pentakills in a game but...let's cheat ok
                        pentaKills=1 if player_info.battleDetail.highestMultiKill == 5 else 0,
                    ),
                    runes=[
                        LolGamePlayerRune(id=rune_info.runeId, slot=idx)
                        for idx, rune_info in enumerate(player_info.perkRunes)
                    ],
                    # They use the same trigrams as we do (TOP MID BOT SUP) except for jungle (JUN instead of JGL)
                    role=player_info.playerLocation
                    if player_info.playerLocation != "JUN"
                    else "JGL",
                    inGameName=player_info.playerName,
                    summonerSpells=[
                        LolGamePlayerSummonerSpell(id=player_info.spell1Id, slot=0),
                        LolGamePlayerSummonerSpell(id=player_info.spell2Id, slot=1),
                    ],
                )

                setattr(
                    lol_player.sources,
                    lol_qq_parser.utils.Config.source_prefix,
                    series_dto.LolQQPlayerSource(
                        id=player_info.playerId,
                        picture_url=player_info.playerAvatar,
                    ),
                )

                lol_team.players.append(lol_player)

            # Finally, we write the team information to our object
            team_side = "BLUE" if team_info.teamId == game_info.blueTeam else "RED"

            setattr(lol_game.teams, team_side, lol_team)

        lol_series.games.append(lol_game)

    return lol_series

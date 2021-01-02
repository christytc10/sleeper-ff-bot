from sportsreference.nfl.boxscore import Boxscores

NFL_API_TO_SLEEPER_TEAMS = {
    "atl": "ATL",
    "buf": "BUF",
    "car": "CAR",
    "chi": "CHI",
    "cin": "CIN",
    "cle": "CLE",
    "clt": "IND",
    "crd": "ARI",
    "dal": "DAL",
    "den": "DEN",
    "det": "DET",
    "gnb": "GB",
    "htx": "HOU",
    "jax": "JAX",
    "kan": "KC",
    "mia": "MIA",
    "min": "MIN",
    "nor": "NO",
    "nwe": "NE",
    "nyg": "NYG",
    "nyj": "NYJ",
    "oti": "TEN",
    "phi": "PHI",
    "pit": "PIT",
    "rai": "LV",
    "ram": "LAR",
    "rav": "BAL",
    "sdg": "LAC",
    "sea": "SEA",
    "sfo": "SF",
    "tam": "TB",
    "was": "WAS",
}


def get_teams_playing(year: int, week: int):
    teams_playing = []
    games = Boxscores(week, year)
    # Prints a dictionary of all games from weeks 7 and 8 in 2017
    for game in games.games:
        nfl_games = games.games.get(game)
        for nfl_game in nfl_games:
            teams_playing.append(NFL_API_TO_SLEEPER_TEAMS.get(nfl_game['home_abbr']))
            teams_playing.append(NFL_API_TO_SLEEPER_TEAMS.get(nfl_game['away_abbr']))
    return teams_playing

from sleeper_wrapper import Players, League, User
from discord_bot.nfl_api.nfl_fixtures import get_teams_playing
from notifications.bot import get_current_week


def get_injured_starters(league_id=649923060580864000):
    rostered_players = {}
    for roster in League(league_id).get_rosters():
        username = User(roster["owner_id"]).get_username()
        for starter in roster['starters']:
            rostered_players[starter] = username

    teams_playing = get_teams_playing(2020, get_current_week())

    report_strings = []
    players = Players().get_all_players()
    for player in players:
        if player in rostered_players.keys():
            owner = rostered_players.get(player)
            player_obj = players.get(player)
            if player_obj['team'].upper() not in teams_playing:
                report_strings.append(f'{owner} - {player_obj["full_name"]} (BYE)')
                continue
            if "injury_status" in player_obj and player_obj["injury_status"] not in [None, '']:
                report_strings.append(f'{owner} - {player_obj["full_name"]} ({player_obj["injury_status"]})')
    report_strings.sort()
    report_string = "**Starters who are on the injury report:**\n" + "\n".join(report_strings)
    return report_string

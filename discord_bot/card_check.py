from sleeper_wrapper import Players, League, User


def get_injured_starters(league_id=522501269823889408):
    rostered_players = {}
    for roster in League(league_id).get_rosters():
        username = User(roster["owner_id"]).get_username()
        for starter in roster['starters']:
            rostered_players[starter] = username

    report_string = "**Starters who are on the injury report:**\n"
    players = Players().get_all_players()
    for player in players:
        if player in rostered_players.keys():
            player_obj = players.get(player)
            if "injury_status" not in player_obj or player_obj["injury_status"] in [None]:
                continue
            owner = rostered_players.get(player)
            report_string += f'{owner} - {player_obj["full_name"]} ({player_obj["injury_status"]})\n'
    return report_string

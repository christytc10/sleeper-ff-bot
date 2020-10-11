from sleeper_wrapper import Players, League


def get_injured_starters(league_id=522501269823889408):
    rostered_players = []
    for roster in League(league_id).get_rosters():
        rostered_players += roster['starters']

    report_string = "**Starters who are on the injury report:**\n"
    players = Players().get_all_players()
    for player in players:
        if player in rostered_players:
            player_obj = players.get(player)
            if "injury_status" not in player_obj or player_obj["injury_status"] in [None]:
                continue
            report_string += f'{player_obj["full_name"]}: {player_obj["injury_status"]}\n'
    return report_string

from sleeper_wrapper import League, Players, User


def get_injury_report(league_id):
    rostered_players = []
    for roster in League(league_id).get_rosters():
        rostered_players += roster['players']

    report_string = "**Injury Report for currently rostered players:**\n"
    players = Players().get_all_players()
    for player in players:
        if player in rostered_players:
            player_obj = players.get(player)
            if "injury_status" not in player_obj or player_obj["injury_status"] in [None]:
                continue
            if player_obj["injury_body_part"] is None or player_obj["injury_start_date"] is None:
                report_string += f'{player_obj["full_name"]}: {player_obj["injury_status"]}\n'
            else:
                report_string += f'{player_obj["full_name"]}: {player_obj["injury_status"]}, {player_obj["injury_body_part"]} since {player_obj["injury_start_date"]}\n'
    return report_string

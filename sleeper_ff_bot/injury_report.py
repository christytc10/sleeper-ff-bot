from sleeper_wrapper import League, Players


def get_injury_report(league_id=485057710979543040):
    rostered_players = []
    for roster in League(league_id).get_rosters():
        rostered_players += roster['players']

    report_string = "# Injury Report for currently rostered players: \n"
    players = Players().get_all_players()
    for player in players:
        if player in rostered_players:
            player_obj = players.get(player)
            if player_obj["injury_status"] in ['NA', 'DNR', 'Sus', None]:
                continue
            report_string += f'{player_obj["full_name"]}: {player_obj["injury_status"]}, {player_obj["injury_body_part"]} since {player_obj["injury_start_date"]}\n'
    return report_string

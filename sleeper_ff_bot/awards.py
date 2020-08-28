from sleeper_wrapper import League, Players
from espn_stats import player_stats_for_week


def to_cm(height_feet_inches):
    feet = int(height_feet_inches[0])
    inches_end_index = height_feet_inches.find('\"')
    inches = int(height_feet_inches[2:inches_end_index])
    total_inches = inches + (feet * 12)
    return total_inches * 2.54


def get_big_boi(league_id=522501269823889408, season=2020, week=1):
    all_rostered_players = []
    for roster in League(league_id).get_rosters():
        roster_players = []
        for player_id in roster['players']:
            roster_players.append(
                {
                    "sleeper_id": player_id,
                    "roster_id": roster['roster_id']
                }
            )
        all_rostered_players += roster_players

    all_rostered_player_ids = (o['sleeper_id'] for o in all_rostered_players)

    decorated_players = []
    players = Players().get_all_players()
    for player in all_rostered_player_ids:
        player_obj = players.get(player)
        player_with_roster = next((x for x in all_rostered_players if x['sleeper_id'] == player_obj['player_id']), None)
        player_obj['roster_id'] = player_with_roster['roster_id']
        player_obj['height_cm'] = to_cm(player_obj['height'])
        decorated_players.append(player_obj)

    espn_ids = [x['espn_id'] for x in decorated_players if (x['position'] in ['WR'])]
    stats = player_stats_for_week(season, week, espn_ids)
    td_scorers = [x['espn_id'] for x in stats if x['rec_tds'] > 0 or x['rush_tds'] > 0]

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    player_with_td = (x for x in decorated_players if x['espn_id'] in td_scorers)
    for player in player_with_td:
        print(f"Week {week} Big Boi is {player['full_name']} at {player['weight']} lbs and {player['height_cm']}")
        break

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=False)
    player_with_td = (x for x in decorated_players if x['espn_id'] in td_scorers)
    for player in player_with_td:
        print(f"Week {week} Little Boi is {player['full_name']} at {player['weight']} lbs and {player['height']}")
        break

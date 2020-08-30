from sleeper_wrapper import League, Players
from datetime import timedelta, datetime


def to_cm(height_feet_inches):
    feet = int(height_feet_inches[0])
    inches_end_index = height_feet_inches.find('\"')
    inches = int(height_feet_inches[2:inches_end_index])
    total_inches = inches + (feet * 12)
    return total_inches * 2.54


def get_draft_awards(league_id):
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
        if player_obj['position'] not in ['WR', 'RB', 'QB', 'TE']:
            continue
        player_with_roster = next((x for x in all_rostered_players if x['sleeper_id'] == player_obj['player_id']), None)
        player_obj['roster_id'] = player_with_roster['roster_id']
        player_obj['height_cm'] = to_cm(player_obj['height'])
        player_obj['age_days'] = int(
            (datetime.utcnow() - datetime.strptime(player_obj['birth_date'], "%Y-%m-%d")) / timedelta(days=1))
        decorated_players.append(player_obj)

    awards_string = ''

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'QB']:
        awards_string += f"Big Ben Memorial Award for Densest QB: Winner is {player['full_name']} at {player['weight']} lbs and {player['height']}\n"
        break

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'RB']:
        awards_string += f"Chonkiest RB: Winner is {player['full_name']} at {player['weight']} lbs and {player['height']}\n"
        break

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'WR']:
        awards_string += f"Thiccest WR: Winner is {player['full_name']} at {player['weight']} lbs and {player['height']}\n"
        break

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'TE']:
        awards_string += f"Big Boi: Winner is {player['full_name']} at {player['weight']} lbs and {player['height']}\n"
        break

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=False)
    for player in decorated_players:
        awards_string += f"Slim Pickens Award: Winner is {player['full_name']} at {player['height']} and {player['weight']} lbs\n"
        break

    decorated_players.sort(key=lambda x: int(x['height_cm']), reverse=False)
    for player in decorated_players:
        awards_string += f"Little Boi: Winner is {player['full_name']} at {player['height']}\n"
        break

    players_on_depth_chart = [x for x in decorated_players if x['depth_chart_order'] is not None]
    players_on_depth_chart.sort(key=lambda a: a['depth_chart_order'], reverse=True)
    for player in players_on_depth_chart:
        awards_string += f"Biggest Swing For The Fences: Winner is {player['full_name']} at {player['depth_chart_order']} on the depth chart\n"
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=False)
    for player in decorated_players:
        awards_string += f"Younghoe Koo Award: Winner is {player['full_name']} at {player['age']} years old\n"
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'WR']:
        awards_string += f"Larry Fitzgerald For Being an NFL Wide Receiver at Age 37: Winner is {player['full_name']} at {player['age']} years old\n"
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'TE']:
        awards_string += f"So Washed He Has To be Justified (Oldest TE): Winner is {player['full_name']} at {player['age']} years old\n"
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=True)
    for player in [x for x in decorated_players if x['position'] == 'RB']:
        awards_string += f"Toddling Back: Winner is {player['full_name']} at {player['age']} years old\n"
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=True)
    for player in decorated_players:
        awards_string += f"Father Time: Winner is {player['full_name']} at {player['age']} years old\n"
        break

    awards_string += f"Grandfather Time: Winner is David Johnson's knees at 63 years old\n"

    return awards_string

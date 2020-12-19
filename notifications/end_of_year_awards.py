from sleeper_wrapper import League, Players
from notifications.espn_stats import player_stats_for_week
from datetime import timedelta, datetime


def to_cm(height_feet_inches):
    feet = int(height_feet_inches[0])
    inches_end_index = height_feet_inches.find('\"')
    inches = int(height_feet_inches[2:inches_end_index])
    total_inches = inches + (feet * 12)
    return total_inches * 2.54


def get_top_stat_for_year(year, stat, players):
    print('TODO - ')
    

def get_big_boi(league_id=522501269823889408, season=2020, week=1):
    all_rostered_players = []
    league = League(league_id)
    for roster in league.get_rosters():
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

    drafts = league.get_all_drafts()
    for draft in drafts:
        print(draft.keys())
        print(draft)
        print(draft['settings']['rounds'])
        exit(1)

    get_top_stat_for_year(2020, 'Targets')

    # TODO - Golden Touch award, highest points per touch in 2020
    # TODO - best sleeper picks
    # TODO - best trade move
    # TODO - FPOE, efficient and inefficient

    decorated_players = []
    players = Players().get_all_players()
    for player in all_rostered_player_ids:
        player_obj = players.get(player)
        player_with_roster = next((x for x in all_rostered_players if x['sleeper_id'] == player_obj['player_id']), None)
        player_obj['roster_id'] = player_with_roster['roster_id']
        player_obj['height_cm'] = to_cm(player_obj['height'])
        player_obj['age_days'] = int(
            (datetime.utcnow() - datetime.strptime(player_obj['birth_date'], "%Y-%m-%d")) / timedelta(days=1))
        decorated_players.append(player_obj)

    print(f'Week {week} awards')

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    for player in (x for x in decorated_players):
        print(f"Big Boi award winner is {player['full_name']} at {player['weight']} lbs and {player['height']}")
        break

    decorated_players.sort(key=lambda x: x['height_cm'], reverse=False)
    player_with_td = (x for x in decorated_players)
    for player in player_with_td:
        print(f"Smol Boi award winner is {player['full_name']} at {player['height']}")
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=True)
    player_with_td = (x for x in decorated_players)
    for player in player_with_td:
        print(f"Jambo Award For Being an Old Bastard winner is {player['full_name']} at {player['age']} years old")
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=False)
    player_with_td = (x for x in decorated_players)
    for player in player_with_td:
        print(f"Drake Award For Promising Youth winner is {player['full_name']} at {player['age']} years old")
        break


print(get_big_boi())

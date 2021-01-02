from sleeper_wrapper import League, Players
from notifications.espn_stats import player_stats_for_week
from datetime import timedelta, datetime


def to_cm(height_feet_inches):
    feet = int(height_feet_inches[0])
    inches_end_index = height_feet_inches.find('\"')
    inches = int(height_feet_inches[2:inches_end_index])
    total_inches = inches + (feet * 12)
    return total_inches * 2.54


def get_big_boi(league_id=649923060580864000, season=2020, week=1):
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
        player_obj['age_days'] = int(
            (datetime.utcnow() - datetime.strptime(player_obj['birth_date'], "%Y-%m-%d")) / timedelta(days=1))
        decorated_players.append(player_obj)

    espn_ids = [x['espn_id'] for x in decorated_players if (x['position'] in ['TE', 'WR', 'RB'])]
    stats = player_stats_for_week(season, week, espn_ids)
    td_scorers = [x['espn_id'] for x in stats if x['rec_tds'] > 0 or x['rush_tds'] > 0]

    print(f'Week {week} awards')

    decorated_players.sort(key=lambda x: int(x['weight']) / x['height_cm'], reverse=True)
    player_with_td = (x for x in decorated_players if x['espn_id'] in td_scorers)
    for player in player_with_td:
        print(f"Big Boi award winner is {player['full_name']} at {player['weight']} lbs and {player['height']}")
        break

    decorated_players.sort(key=lambda x: x['height_cm'], reverse=False)
    player_with_td = (x for x in decorated_players if x['espn_id'] in td_scorers)
    for player in player_with_td:
        print(f"Smol Boi award winner is {player['full_name']} at {player['height']}")
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=True)
    player_with_td = (x for x in decorated_players if x['espn_id'] in td_scorers)
    for player in player_with_td:
        print(f"Jambo Award For Being an Old Bastard winner is {player['full_name']} at {player['age']} years old")
        break

    decorated_players.sort(key=lambda x: int(x['age_days']), reverse=False)
    player_with_td = (x for x in decorated_players if x['espn_id'] in td_scorers)
    for player in player_with_td:
        print(f"Drake Award For Promising Youth winner is {player['full_name']} at {player['age']} years old")
        break

    player_with_td = [x for x in decorated_players if x['espn_id'] in td_scorers and x['depth_chart_order'] is not None]
    player_with_td.sort(key=lambda a: a['depth_chart_order'], reverse=True)
    for player in player_with_td:
        print(
            f"Who the Fuck is Tingis Pingis Award for Coming Out of Nowhere winner is {player['full_name']} at number {player['depth_chart_order']} on the depth chart")
        break

    added_players = []
    fake_league = League(649923060580864000)
    txns = fake_league.get_transactions(week=1)
    for txn in [x['adds'] for x in txns if x['type'] in ['free_agent', 'waiver'] and x['adds'] is not None]:
        for key in txn.keys():
            added_players.append(key)
    print(added_players)


def get_waiver_pickup_award(league_id=517097510076678144, season=2019, week=16):
    league_api = League(league_id)
    waiver_claims = [x for x in league_api.get_transactions(1) if x['type'] == 'waiver']
    players = Players().get_all_players()
    claimed_players= []
    for waiver_claim in waiver_claims:
        claimed_player = players.get(list(waiver_claim['adds'].keys())[0])
        print(f"{claimed_player['first_name']} {claimed_player['last_name']}")
        claimed_players.append(claimed_player)
        #TODO - add who claimed them

    espn_ids = [x['espn_id'] for x in claimed_players]
    print(espn_ids)
    stats = player_stats_for_week(season, week, espn_ids)
    print(stats)
    return 'DONE'


print(get_waiver_pickup_award())

from sleeper_wrapper import Players, League, User
from discord_bot.player_value import find_value

def get_roster_ages(league_id=522501269823889408):
    players = Players().get_all_players()
    rostered_ages = {}

    for roster in League(league_id).get_rosters():
        rostered_players = []
        for player in roster['players']:
            rostered_players.append(players.get(player))
        ages = []
        for x in [p['age'] for p in rostered_players]:
            ages.append(x)
        username = User(roster["owner_id"]).get_username()
        average_age = sum(ages)/len(ages)
        rostered_ages[username] = average_age

    age_string = "Roster Ages:\n"
    sort_orders = sorted(rostered_ages.items(), key=lambda x: x[1], reverse=True)
    for roster_age in sort_orders:
        age_string += f"{roster_age[0]}: {round(roster_age[1], 2)}\n"
    return age_string


def get_roster_value(league_id=522501269823889408):
    players = Players().get_all_players()
    rostered_value = {}

    for roster in League(league_id).get_rosters():
        rostered_players = []
        for player in roster['players']:
            rostered_players.append(players.get(player))
        values = []
        for p in rostered_players:
            values.append(find_value(p['full_name']))
        username = User(roster["owner_id"]).get_username()
        total_value = sum(values)
        rostered_value[username] = total_value

    age_string = "Roster Value (excludes picks and most really low value guys tbh):\n"
    sort_orders = sorted(rostered_value.items(), key=lambda x: x[1], reverse=True)
    for roster_age in sort_orders:
        age_string += f"{roster_age[0]}: {round(roster_age[1], 2)}\n"
    return age_string

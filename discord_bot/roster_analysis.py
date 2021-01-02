from sleeper_wrapper import Players, League, User
from discord_bot.player_value import find_value


def get_roster_ages(league_id=649923060580864000):
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
        average_age = sum(ages) / len(ages)
        rostered_ages[username] = average_age

    age_string = "Roster Ages:\n"
    sort_orders = sorted(rostered_ages.items(), key=lambda x: x[1], reverse=True)
    for roster_age in sort_orders:
        age_string += f"{roster_age[0]}: {round(roster_age[1], 2)}\n"
    return age_string


def get_roster_value(league_id=649923060580864000):
    players = Players().get_all_players()
    return_string = "Position Values (excludes dross ;) ):\n"

    for roster in League(league_id).get_rosters():
        username = User(roster["owner_id"]).get_username()
        return_string += f'{username}:\n'
        values = {}
        for player in roster['players']:
            p = players.get(player)
            if p['position'] not in values:
                values[p['position']] = find_value(p['full_name'])
            else:
                values[p['position']] = values[p['position']] + find_value(p['full_name'])
        for x in sorted(values):
            return_string += f'{x}:{round(values.get(x),2)}\n'
        return_string += '\n'
    return return_string

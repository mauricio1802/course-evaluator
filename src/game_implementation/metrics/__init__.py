


def round_iterator(states):
    actual_round = states[0].round

def compute_stability_metric(states):
    players = {}
    for player in states[0].players():
        player_id = player.get_id()
        players[player_id] = []
from statistics import mean, stdev
from ..utils import get_player_score, round_iterator
from ..state import Professor, Student


def compute_positions(states):
    first_state = states[0]
    last_state = states[-1]
    players = list(filter(lambda p: isinstance(p, Student), first_state.players))
    scores = []
    for player in players:
        start_score = get_player_score(first_state, player.get_id())
        end_score = get_player_score(last_state, player.get_id())
        scores.append((end_score - start_score, player.get_id()))
    return sorted(scores, reverse=True)


def is_stable(last_position, positions_mean, positions_stdev):
    return abs(last_position - positions_mean) <= positions_stdev


def compute_stability_metric(states):
    players = {}
    metric = 0
    last_positions = {}
    for player in filter(lambda p: isinstance(p, Student), states[0].players):
        player_id = player.get_id()
        players[player_id] = []
    
    for states_round in round_iterator(states):
        positions = compute_positions(states_round)
        for i, (_, player_id) in enumerate(positions, 1):
            players[player_id].append(i)
    
    final_positions = compute_positions(states)
    for i, (_, player_id) in enumerate(final_positions, 1):
        last_positions[player_id] = i

    for player in players.keys():
        positions = players[player]
        positions_mean = mean(positions)
        positions_stdev = stdev(positions)
        last_position = last_positions[player]
        if not is_stable(last_position, positions_mean, positions_stdev):
            metric += 1
    return metric
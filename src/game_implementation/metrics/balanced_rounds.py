from ..utils import round_iterator, rounds_window, get_round_number, total_achievable_points_in_round, total_achievable_points_in_state


def is_balance(round_to_check, rounds_to_check_against):
    points_in_round_to_check = total_achievable_points_in_round(round_to_check)
    points_in_rest_rounds = sum(
        map(lambda round: points_in_round_to_check(round), rounds_to_check_against))
    return points_in_round_to_check < points_in_rest_rounds


def balanced_rounds_metric(states):
    unbalance_rounds = set()
    for round_set in rounds_window(round_iterator(states), 4):
        first_round = round_set[0]
        if not is_balance(first_round, round_set[1:]):
            unbalance_rounds.add(get_round_number(first_round))
        last_round = round_set[-1]
        if not is_balance(last_round, round_set[:-1]):
            unbalance_rounds.add(get_round_number(last_round))
    return len(unbalance_rounds)

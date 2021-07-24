from ..utils import round_iterator, total_achievable_points_in_round
from statistics import mean


def achievable_points_trend(states):
    metric = 0
    rounds_points = []
    means = [0]
    for round_to_check in round_iterator(states):
        points = total_achievable_points_in_round(round_to_check)
        rounds_points.append(points)
        means.append(mean(rounds_points))
        if means[-1] < means[-2]:
            metric += 1
    return metric
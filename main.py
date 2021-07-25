import logging
from src.game_implementation import NumericGame, Student, Professor, state_repr
from src.game import Play, GameEnded
from src.game_implementation.players import StudentHumanPlayer, ProfessorHumanPlayer
from src.game_implementation.metrics import achievable_points_trend, compute_stability_metric, balanced_rounds_metric
from src.logging import LoggerFactory

LOGGER = LoggerFactory("NumericGame")
LOGGER.setLevel(logging.INFO)

players = [
    StudentHumanPlayer(None, 0.5, 6),
    StudentHumanPlayer(None, 0.3, 3),
    ProfessorHumanPlayer(None)
]

match = NumericGame.get_match(players)

while True:
    state = match.get_current_state()
    # print(state_repr(state))
    try:
        match.move()
    except GameEnded as e:
        print(e)
        states = match.states
        print("Stability")
        print(compute_stability_metric(states))
        print("Balanced")
        print(balanced_rounds_metric(states))
        print("Trend")
        print(achievable_points_trend(states))



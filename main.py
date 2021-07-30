import logging
from src.game_implementation import (
    NumericGame, 
    Student, 
    Professor, 
    SolveChallenge, 
    AddChallengePayload, 
    RemoveChallengePayload, 
    ChallengeDefinition, 
    Challenge,
    player_repr 
)
from src.game import Play, GameEnded
from src.game_implementation.players import StudentHumanPlayer, ProfessorHumanPlayer, ProfessorPlanPlayer, StudentGreedyPlayer, StudentOptimalPlayer
from src.game_implementation.metrics import achievable_points_trend, compute_stability_metric, balanced_rounds_metric
from src.logging import LoggerFactory

LOGGER = LoggerFactory("NumericGame")
LOGGER.setLevel(logging.INFO)

PROFESSOR_PLAN = [
    [
        Play(
            "set_challenge",
            AddChallengePayload(
                Challenge(
                    1,
                    ChallengeDefinition(0, 10, 15),
                    2
                )
            )
        ),
        Play(
            "set_challenge",
            AddChallengePayload(
                Challenge(
                    2,
                    ChallengeDefinition(0, 10, 10),
                    3
                )
            )
        ),
        Play("finish_turn", None)
    ],
    [
        Play(
            "set_challenge",
            AddChallengePayload(
                Challenge(
                    3,
                    ChallengeDefinition(0, 10, 15),
                    2
                )
            )
        ),
        Play(
            "set_challenge",
            AddChallengePayload(
                Challenge(
                    4,
                    ChallengeDefinition(0, 10, 10),
                    3
                )
            )
        ),
        Play("finish_turn", None)
    ],
    [
        Play(
            "set_challenge",
            AddChallengePayload(
                Challenge(
                    4,
                    ChallengeDefinition(0, 10, 40),
                    4
                )
            )
        ),
        Play(
            "set_challenge",
            AddChallengePayload(
                Challenge(
                    5,
                    ChallengeDefinition(0, 10, 5),
                    2
                )
            )
        ),
        Play("finish_turn", None)

    ]
]

players = [
    # StudentHumanPlayer(None, 0.5, 6),
    # StudentHumanPlayer(None, 0.5, 3),
    # StudentHumanPlayer(None, 0.5, 5),
    # StudentGreedyPlayer(None, 0.5, 6),
    StudentOptimalPlayer(None, 0.5, 6),
    StudentGreedyPlayer(None, 0.5, 3),
    StudentGreedyPlayer(None, 0.5, 5),
    ProfessorPlanPlayer(None, PROFESSOR_PLAN)
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
        last_state = states[-1]
        players = list(filter(lambda p: isinstance(p, Student), last_state.players))
        for player in players:
            print(player_repr(player))        
        print("Stability")
        print(compute_stability_metric(states))
        print("Balanced")
        print(balanced_rounds_metric(states))
        print("Trend")
        print(achievable_points_trend(states))
        break



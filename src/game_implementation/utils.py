from .state import Student, Professor


def print_professor(player):
    print("Professor")
    print(f"Id: {player.player_id}")


def print_student(player):
    print("Student")
    print(f"Id: {player.player_id}")
    print(f"Score: {player.score}")
    print(f"Energy: {player.energy}")
    print(f"Interest Base: {player.base_interest}")
    print(f"Interest Variable: {player.variable_interest}")
    print(f"Ability: {player.ability}")


def print_player(player):
    if isinstance(player, Student):
        print_student(player)
    if isinstance(player, Professor):
        print_professor(player)

def print_challenge(challenge):
    print(f"Id: {challenge.get_id()}")
    print(f"Student allowed: {challenge.student_allowed}")
    print(f"Interest required: {challenge.interest_required}")
    print(f"Cost: {challenge.cost}")
    print(f"Reward: {challenge.reward}")


def print_state(state):
    print()
    print(f"Actual Player: {state.actual_player}")
    print(f"Round: {state.round}")
    print()
    print("///////////////////////////////////////")
    print("Players:")
    for player in state.players:
        print_player(player)
        print()
    print()
    print("///////////////////////////////////////")
    print("Challenges:")
    for challenge in state.challenges:
        print_challenge(challenge)
        print()
    print()
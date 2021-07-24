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


def get_player_score(state, player_id):
    for player in state.players:
        if player.get_id() == player_id:
            return player.score


def round_iterator(states):
    actual_round = states[0].round
    actual_round_states = []

    for state in states:
        if state.round == actual_round:
            actual_round_states.append(states)
        else:
            yield actual_round_states
            actual_round_states = [ state ]
            actual_round = state.round


def rounds_window(rounds, window_size):
    window = []
    for r in rounds:
        window.append(r)
        if len(window) == window_size:
            yield window
            window.pop(0)


def get_round_number(round_to_check):
    return round_to_check[0].round


def total_achievable_points_in_state(state_to_check):
    challenges = state_to_check.challenges
    return sum(map(lambda challenge: challenge.reward, challenges))


def total_achievable_points_in_round(round_to_check):
    return sum(map(lambda state: total_achievable_points_in_state(state), round_to_check))
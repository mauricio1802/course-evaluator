from .state import Student, Professor


def professor_repr(player):
    return f"Id: {player.player_id}"


def student_repr(player):
    return f"""
    Id: {player.player_id}
    Score: {player.score}
    Energy: {player.energy}
    Interest Base: {player.base_interest}
    Interest Variable: {player.variable_interest}
    Ability: {player.ability}
    """


def player_repr(player):
    if isinstance(player, Student):
        return student_repr(player)
    if isinstance(player, Professor):
        return professor_repr(player)

def challenge_repr(challenge):
    return f"""
    Id: {challenge.get_id()}
    Student allowed: {challenge.student_allowed}
    Interest required: {challenge.interest_required}
    Cost: {challenge.cost}
    Reward: {challenge.reward}
    """


def state_repr(state):
    players_str = "\n".join(map(player_repr, state.players))
    challenges_str = "\n".join(map(challenge_repr, state.challenges))
    return f"""
    Actual Player: {state.actual_player}
    Round: {state.round}

    ///////////////////////////////////////

    Players:
    {players_str}

    ///////////////////////////////////////

    Challenges:
    {challenges_str}
    """

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
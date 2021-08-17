import numpy as np
from typing import List
from src.game_implementation import GameState, Challenge, ChallengeDefinition, Student


def challenge_to_tensor(challenge: Challenge):
    challenge_definition: ChallengeDefinition = challenge._challenge_definition
    return np.array([
        challenge_definition.interest_required, 
        challenge_definition.reward, 
        challenge_definition.cost
    ])

def challenges_to_tensor(challenges: List[Challenge]):
    num_of_challenges = len(challenges)
    challenges_rep = np.zeros(3)
    if num_of_challenges != 0:
        challenges_rep = np.array(list(map(lambda c: challenge_to_tensor(c), challenges))).sum(0)
    return np.append(num_of_challenges, challenges_rep)

def player_to_tensor(player: Student):
    return np.array([
        player.player_id,
        player.score,
        player.energy,
        player.interest
    ])


def player_and_challenges_to_tensor(state: GameState, player_id: int):
    players = state.players
    player_state = list(filter(lambda p: p.get_id() == player_id, players))[0]
    
    challenges = state.challenges
    player_challenges = list(filter(lambda c: c.student_allowed == player_id, challenges))

    challenges_tensor = challenges_to_tensor(player_challenges)
    player_tensor = player_to_tensor(player_state)

    unnormalize_tensor = np.append(player_tensor, challenges_tensor)
    norm = np.linalg.norm(unnormalize_tensor)
    return unnormalize_tensor / norm

def state_to_tensor(state: GameState):
    players: List[Student] = state.players
    return np.stack(list(map(lambda p: player_and_challenges_to_tensor(state, p.get_id()), players)))



def create_neuron(num_of_players):
    return np.random.random((8, 4))


### Player X 8 

import numpy as np
from typing import List
from ....game import Player, Play
from ...game import AddChallengePayload, RemoveChallengePayload
from ...state import ChallengeDefinition, ChallengeDefinition, Challenge, Professor, Student, GameState


class MLProfessor(Professor, Student):
    def __init__(self, id, neuron):
        Professor.__init__(self, id)
        self._neuron = neuron
        self._last_challenge_id = 0

    def set_id(self, id):
        self.player_id = id
    
    def get_id(self):
        return self.player_id
    
    def play(self, states):
        pass

    def _get_challenge_id(self):
        self._last_challenge_id += 1
        return self._last_challenge_id
    

    @staticmethod
    def _challenge_to_tensor(challenge: Challenge):
        challenge_definition: ChallengeDefinition = challenge._challenge_definition
        return np.array([
            challenge_definition.interest_required, 
            challenge_definition.reward, 
            challenge_definition.cost
        ])

    @staticmethod
    def _challenges_to_tensor(challenges: List[Challenge]):
        num_of_challenges = len(challenges)
        challenges_rep = np.zeros(3)
        if num_of_challenges != 0:
            challenges_rep = np.array(list(map(lambda c: MLProfessor._challenge_to_tensor(c), challenges))).sum(0)
        return np.append(num_of_challenges, challenges_rep)

    @staticmethod
    def _player_to_tensor(player: Student):
        return np.array([
            player.player_id,
            player.score,
            player.energy,
            player.interest
        ])


    @staticmethod
    def _player_and_challenges_to_tensor(state: GameState, player_id: int):
        players = state.players
        player_state = list(filter(lambda p: p.get_id() == player_id, players))[0]
        
        challenges = state.challenges
        player_challenges = list(filter(lambda c: c.student_allowed == player_id, challenges))

        challenges_tensor = MLProfessor._challenges_to_tensor(player_challenges)
        player_tensor = MLProfessor._player_to_tensor(player_state)

        unnormalize_tensor = np.append(player_tensor, challenges_tensor)
        norm = np.linalg.norm(unnormalize_tensor)
        return unnormalize_tensor / norm

    @staticmethod
    def _state_to_tensor(state: GameState):
        players: List[Student] = state.players
        return np.stack(list(map(lambda p: MLProfessor._player_and_challenges_to_tensor(state, p.get_id()), players)))

    @staticmethod
    def _decode_play_type(value):
        if value < 0.33:
            return 'finish_turn' 
        if value < 0.66:
            return 'remove_challenge'
        return 'set_challenge'

    @staticmethod
    def _decode_play(encoded_play, state):
        play_type = MLProfessor._decode_play_type(encoded_play[0])
        if play_type == 'finish_turn':
            pass
        if play_type == 'set_challenge':
            pass
        if play_type == 'remove_challenge':
            pass
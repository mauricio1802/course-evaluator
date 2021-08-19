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

    def _decode_play_type(self, value):
        if value < 0.33:
            return 'finish_turn' 
        if value < 0.66:
            return 'remove_challenge'
        return 'set_challenge'

    def _define_player(self, value, number_of_players):
        seg_length = 1 / number_of_players
        seg = value // seg_length
        return seg + 1
    
    def _decode_cost(self, value):
        return value * 1000
    
    def _decode_reward(self, value):
        return value * 10000
    
    def _decode_add_challenge_payload(self, encoded_play, state):
        number_of_players = len(state.players)
        player = self._define_player(encoded_play[1], number_of_players)

        interest_required = encoded_play[2]
        cost = self._decode_cost(encoded_play[3])
        reward = self._decode_reward(encoded_play[4])
        
        challenge_id = self._get_challenge_id()
        challenge_definition = ChallengeDefinition(interest_required, cost, reward)
        return Challenge(challenge_id ,challenge_definition, player)
    
    def _decode_remove_challenge_payload(self, encoded_play, state):
        pass

    def _decode_play(self, encoded_play, state):
        play_type = self._decode_play_type(encoded_play[0])
        if play_type == 'finish_turn':
            return Play('finish_turn', None)

        if play_type == 'set_challenge':
            add_challenge_payload = self._decode_add_challenge_payload(encoded_play, state)
            return Play('set_challenge', add_challenge_payload)

        if play_type == 'remove_challenge':
            remove_challenge_payload = self._decode_remove_challenge_payload(encoded_play, state)
            return Play('remove_challenge', remove_challenge_payload)
from ....game import Play
from ...state import ChallengeDefinition, Challenge, Professor
from ...game import AddChallengePayload, RemoveChallengePayload
from ....game import Player

class ProfessorHumanPlayer(Professor, Player):
    def __init__(self, id):
        Professor.__init__(self, id)
        self._last_challenge_id = 0
    
    def set_id(self, id):
        self.player_id = id
    
    def _get_challenge_id(self):
        self._last_challenge_id += 1
        return self._last_challenge_id
    
    def play(self, states):
        play_type = int(input("Select play: "))
        if play_type == 1:
            return Play("finish_turn", None)
        elif play_type == 2:
            interest_required = float(input("Interest required: "))
            cost = int(input("Insert cost: ")) 
            reward = int(input("Insert reward: "))
            student_id = int(input("Student allowed to solve: "))
            challenge_id = self._get_challenge_id()
            challenge_definition = ChallengeDefinition(interest_required, cost, reward)
            challenge = Challenge(challenge_id, challenge_definition, student_id)
            payload = AddChallengePayload(challenge)
            return Play("set_challenge", payload)
        elif play_type == 3:
            id_to_remove = int(input("Challenge to remove: "))
            payload = RemoveChallengePayload(challenge_id=id_to_remove)
            return Play("remove_challenge", payload)
    
    def get_id(self):
        return self.player_id
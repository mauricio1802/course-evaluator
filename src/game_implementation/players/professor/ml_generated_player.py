from ....game import Player, Play
from ...game import AddChallengePayload, RemoveChallengePayload
from ...state import ChallengeDefinition, ChallengeDefinition, Challenge, Professor, Student


class MLProfessor(Professor, Student):
    def __init__(self, id):
        Professor.__init__(self, id)

    def set_id(self, id):
        self.player_id = id
    
    def get_id(self):
        return self.player_id
    
    def play(self, states):
        pass
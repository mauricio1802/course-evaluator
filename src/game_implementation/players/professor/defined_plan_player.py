from ...state import Professor
from ....game import Player

class ProfessorPlanPlayer(Professor, Player):
    def __init__(self, id, plan):
        Professor.__init__(self, id)
        self._last_challenge_id = 0
        self._plan = plan
    
    def set_id(self, id):
        self.player_id = id
    
    def _get_challenge_id(self):
        self._last_challenge_id += 1
        return self._last_challenge_id
    
    def play(self, states):
        actual_round = states[-1].round
        round_plan = self._plan[actual_round - 1]
        return round_plan.pop(0)
    
    def get_id(self):
        return self.player_id
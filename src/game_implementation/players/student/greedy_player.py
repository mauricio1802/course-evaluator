from ....game import Play
from ...state import Student
from ...game import SolveChallenge
from ....game import Player
from ...utils import challenge_repr

class StudentGreedyPlayer(Student, Player):
    def __init__(self, id, base_interest, ability):
        Student.__init__(self, id, base_interest, ability)
    
    def set_id(self, id):
        self.player_id = id

    def play(self, states):
        actual_state = states[-1]
        challenges = actual_state.challenges
        doable_challenges = self._get_doable_challenges(actual_state)
        if len(doable_challenges) == 0:
            return Play("finish_turn", None)
        selected_challenge = self._challenge_with_max_reward(doable_challenges) 
        return Play("solve_challenge", SolveChallenge(selected_challenge.get_id()))
        
    def get_id(self):
        return self.player_id
    
    def _get_allowed_challenges(self, state):
        challenges = state.challenges
        return list(filter(lambda c: c.student_allowed == self.player_id, challenges))

    def _get_doable_challenges(self, state):
        allowed_challenges = self._get_allowed_challenges(state)
        players = state.players
        me = next(filter(lambda p: p.get_id() == self.get_id(), players))
        maximum_points = me.energy * me.ability
        return list(filter(lambda c: c.interest_required <= me.interest and c.cost <= maximum_points, allowed_challenges))
    
    def _challenge_with_max_reward(self, challenges):
        best_challenge = None
        max_reward = 0
        for challenge in challenges:
            if challenge.reward > max_reward:
                max_reward = challenge.reward
                best_challenge = challenge
        return best_challenge
    
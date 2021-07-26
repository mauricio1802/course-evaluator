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
        my_challenges = list(filter(lambda c: c.student_allowed == self.player_id, challenges))
        if len(my_challenges) == 0:
            return Play("finish_turn", None)
        return Play("solve_challenge", SolveChallenge(my_challenges[0].get_id()))
        
    def get_id(self):
        return self.player_id
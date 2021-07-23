
from ....game import Play
from ...state import Student
from ...game import SolveChallenge
from ....game import Player


class StudentHumanPlayer(Student, Player):
    def __init__(self, id, base_interest, ability):
        Student.__init__(self, id, base_interest, ability)
    
    def set_id(self, id):
        self.player_id

    def play(self, states):
        play_type = int(input("Select play: "))
        if play_type == 1:
            return Play("finish_turn", None)
        elif play_type == 2:
            challenge_to_solve = int(input("Insert challenge to solve: "))
            payload = SolveChallenge(challenge_to_solve)
            return Play("solve_challenge", payload)
    
    def get_id(self):
        return self.player_id
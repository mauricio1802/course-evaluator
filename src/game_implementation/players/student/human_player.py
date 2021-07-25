from ....game import Play
from ...state import Student
from ...game import SolveChallenge
from ....game import Player
from ...utils import challenge_repr

class StudentHumanPlayer(Student, Player):
    def __init__(self, id, base_interest, ability):
        Student.__init__(self, id, base_interest, ability)
    
    def set_id(self, id):
        self.player_id = id

    def play(self, states):
        play_type = int(input("""Select play: 
        1 - End turn
        2 - Solve challenge\n"""))
        if play_type == 1:
            return Play("finish_turn", None)
        elif play_type == 2:
            challenges_str = "\n".join(map(challenge_repr, states[-1].challenges))
            print(f"""Challenges: 
            {challenges_str}""")
            challenge_to_solve = int(input("Insert challenge to solve: "))
            payload = SolveChallenge(challenge_to_solve)
            return Play("solve_challenge", payload)
    
    def get_id(self):
        return self.player_id
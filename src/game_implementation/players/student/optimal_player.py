from ....game import Play
from ...state import Student
from ...game import SolveChallenge
from ....game import Player
from ...utils import challenge_repr
from pulp import LpProblem, LpMaximize, LpVariable, LpBinary, lpSum, PULP_CBC_CMD


class StudentOptimalPlayer(Student, Player):
    def __init__(self, id, base_interest, ability):
        Student.__init__(self, id, base_interest, ability)
        self.challenges_to_solve = []
    
    def set_id(self, id):
        self.player_id = id

    def play(self, states):
        actual_state = states[-1]
        if self.challenges_to_solve == []:
            self.challenges_to_solve = self._select_challenges_to_solve(actual_state)

        if self.challenges_to_solve == []:
            return Play("finish_turn", None)
        
        challenge_to_solve = self.challenges_to_solve.pop(0)
        return Play("solve_challenge", SolveChallenge(challenge_to_solve))

    def get_id(self):
        return self.player_id
    
    def _get_my_actual_state(self, state):
        players = state.players
        return next(filter(lambda p: p.get_id() == self.get_id(), players))

    def _get_maximum_points(self, state):
        me = self._get_my_actual_state(state)
        return me.energy * me.ability
    
    def _get_allowed_challenges(self, state):
        challenges = state.challenges
        return list(filter(lambda c: c.student_allowed == self.player_id, challenges))

    def _get_doable_challenges(self, state):
        allowed_challenges = self._get_allowed_challenges(state)
        me = self._get_my_actual_state(state)
        maximum_points = self._get_maximum_points(state)
        return list(filter(lambda c: c.interest_required <= me.interest and c.cost <= maximum_points, allowed_challenges))
    
    def _select_challenges_to_solve(self, state):
        challenges = self._get_doable_challenges(state)
        if challenges == []:
            return []
        maximum_points = self._get_maximum_points(state)
        model = LpProblem(sense=LpMaximize)
        model.setSolver(PULP_CBC_CMD(msg=0))
        variables = [LpVariable(name=f"{challenge.get_id()}", cat=LpBinary) for challenge in challenges]
        model += lpSum([challenge.cost *variables[i] for i, challenge in enumerate(challenges)]) <= maximum_points
        model += lpSum([challenge.reward*variables[i] for i, challenge in enumerate(challenges)])
        model.solve()
        return [int(var.name) for var in model.variables()]
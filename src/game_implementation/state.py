from typing import List
from ..game import State, Player, Id
from .fuzzy_system_var_interest import MockInterest


class PlayerRepresentation:
    def __init__(self, id):
        self.player_id = id
    

class Professor(PlayerRepresentation):
    def __init__(self, id):
        super().__init__(id)


class Student(PlayerRepresentation):
    def __init__(self, id, base_interest, ability):
        super().__init__(id)
        self.energy = 100
        self.score = 0
        self.base_interest = base_interest 
        self.ability = ability
    
    @property
    def variable_interest(self):
        return MockInterest.get_variable_interest()


class ChallengeDefinition:
    def __init__(self, interest_required: float, cost: int, reward: int):
        self.interest_required: float = interest_required
        self.cost: int = cost
        self.reward: int = reward


class Challenge:
    def __init__(self, id: Id, challenge_definition: ChallengeDefinition, student_can_solve: Student):
        self._id: Id = id
        self._challenge_definition: ChallengeDefinition = challenge_definition
        self._student_can_solve: Student = student_can_solve 
    
    @property
    def interest_required(self) -> float:
        return self._challenge_definition.interest_required
    
    @property
    def cost(self) -> int:
        return self._challenge_definition.cost
    
    @property
    def reward(self) -> int:
        return self._challenge_definition.reward
    
    @property
    def student_allowed(self) -> Id:
        return self._student_can_solve
    
    def get_id(self) -> Id:
        return self._id


class GameState(State):
    round: int
    challenges: List[Challenge]
    players: List[PlayerRepresentation]
    actual_player: Id
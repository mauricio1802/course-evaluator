from typing import List
from copy import deepcopy 
from random import shuffle
from ..game import Id, Play, PlayPayload, Game, Match, Player
from .state import GameState, Student, Professor, Challenge
from ..logging import LoggerFactory
from .utils import challenge_repr, state_repr


LOGGER = LoggerFactory("NumericGame").getChild("Game")

class AddChallengePayload(PlayPayload):
    challenge: Challenge


class RemoveChallengePayload(PlayPayload):
    challenge_id: Id


class SolveChallenge(PlayPayload):
    challenge_id: Id 


class PlayerStateFactory:
    def __init__(self):
        self._last_id = 0
    
    def build_student_state(self, ability, interest_base):
        self._last_id += 1
        student = Student(self._last_id, interest_base, ability)
        return student
    
    def build_professor_state(self):
        self._last_id += 1
        professor = Professor(self._last_id)
        return professor


class NumericGame(Game):
    round_number = 4
    function_per_play = {
        'solve_challenge': lambda cls: cls._play_solve_challenge,
        'finish_turn': lambda cls: cls._play_finish_turn,
        'set_challenge': lambda cls: cls._play_set_challenge,
        'remove_challenge': lambda cls: cls._play_remove_challenge
    }

    @staticmethod
    def get_match(players: List[Player]) -> Match:
        LOGGER.info("Creating Match")
        players_factory = PlayerStateFactory()
        professor = players_factory.build_professor_state()
        students = []
        professor_player = next(filter(lambda p : isinstance(p, Professor), players))
        professor_player.set_id(professor.get_id())
        for player in filter(lambda p : isinstance(p, Student), players):
            new_student = players_factory.build_student_state(player.ability, player.base_interest)
            player.set_id(new_student.get_id())
            students.append(new_student)
        shuffle(students)
        initial_state = GameState(
            round = 1,
            challenges = [],
            players = [professor] + students,
            actual_player = professor.player_id
        ) 
        return Match(initial_state, NumericGame, players)

    
    @staticmethod
    def get_visible_states(states: List[GameState], player: Player) -> List[GameState]:
        return states
    
    @staticmethod
    def get_current_player(states: List[GameState], players: List[Player]) -> Player:
        actual_player_id = states[-1].actual_player
        return next(filter(lambda player: player.get_id() == actual_player_id, players))
    
    @classmethod
    def update_state(cls, actual_state: GameState, play: Play) -> GameState:
        transition_function = NumericGame.function_per_play[play.name](cls)
        return transition_function(actual_state, play.payload)
    
    @staticmethod
    def is_final_state(state):
        if state.round == NumericGame.round_number:
            return True
        return False
    
    @staticmethod
    def _play_solve_challenge(actual_state: GameState, play: PlayPayload) -> GameState:
        # getting challenge to solve
        challenge_index, challenge_to_solve = 0, None 
        for i, challenge in enumerate(actual_state.challenges):
            if challenge.get_id() == play.challenge_id:
                challenge_to_solve = challenge
                challenge_index = i

        # getting solver
        solver_index, solver = 0, None
        for i, player in enumerate(actual_state.players):
            if player.player_id == actual_state.actual_player:
                solver = player
                solver_index = i
        
        if NumericGame._can_solve(solver, challenge_to_solve):
            LOGGER.info(f"Player with id {solver.get_id()} solved challenge with id {challenge.get_id()}")
            new_challenges = deepcopy(actual_state.challenges)
            new_challenges.pop(challenge_index)
            new_players = deepcopy(actual_state.players)
            new_players[solver_index].score += challenge_to_solve.reward
            used_energy = NumericGame._compute_energy(solver, challenge_to_solve)
            new_players[solver_index].energy -= used_energy
            new_state = GameState(
                round = actual_state.round,
                challenges = new_challenges,
                players = new_players,
                actual_player = actual_state.actual_player
            )
            return new_state

        return actual_state

    @staticmethod
    def _play_finish_turn(actual_state: GameState, play: PlayPayload) -> GameState:
        players = actual_state.players
        actual_player_index = 0
        actual_player_id = actual_state.actual_player
        LOGGER.info(f"Player with id {actual_player_id} finish her/his turn")

        for i, player in enumerate(players):
            if player.player_id == actual_player_id:
                actual_player_index = i
        new_player_index = (actual_player_index + 1) % len(players)
        new_players = actual_state.players

        if new_player_index == 0:
            new_players = deepcopy(new_players)
            for player in filter(lambda p: isinstance(p, Student), new_players):
                player.update_variable_interest()
                player.energy = 100

        new_state = GameState(
            round = actual_state.round + 1 if new_player_index == 0 else actual_state.round,
            challenges = actual_state.challenges,
            players = new_players,
            actual_player = players[new_player_index].get_id()
        )
        return new_state
    
    @staticmethod
    def _play_set_challenge(actual_state: GameState, play: PlayPayload) -> GameState:
        LOGGER.info("Professor is adding a Challenge")
        LOGGER.info(f"""Challenge added:
                        {challenge_repr(play.challenge)}""")
        new_challenges = deepcopy(actual_state.challenges)
        new_challenges.append(play.challenge)
        new_state = GameState(
            round = actual_state.round,
            players = actual_state.players,
            challenges = new_challenges,
            actual_player = actual_state.actual_player
        )
        return new_state
    
    @staticmethod
    def _play_remove_challenge(actual_state: GameState, play: PlayPayload) -> GameState:
        challenge_to_remove = play.challenge_id
        new_challenges = deepcopy(actual_state.challenges)
        for i, challenge in enumerate(new_challenges):
            if challenge.get_id() == challenge_to_remove:
                new_challenges.pop(i)
                break
        new_state = GameState(
            round = actual_state.round,
            players = actual_state.players,
            challenges = new_challenges,
            actual_player = actual_state.actual_player
        )
        return new_state
    
    @staticmethod
    def _compute_energy(player, challenge):
        return challenge.cost / player.ability
    
    @staticmethod
    def _can_solve(player, challenge):
        if player.get_id() != challenge.student_allowed:
            return False
        energy_require = NumericGame._compute_energy(player, challenge)
        player_interest = min(1, player.interest)
        return energy_require <= player.energy and challenge.interest_required <= player_interest
    


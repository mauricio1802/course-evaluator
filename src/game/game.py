from typing import List
from abc import ABC, abstractmethod
from collections import namedtuple
from .state import State
from .player import Player, Play


class GameEnded(Exception):
    pass


class Match:
    def __init__(self, initial_state: State, game_engine, players: List[Player]):
        self._states: List[State] = [initial_state]
        self._players: List[Player] = players
        self._game_engine: Game = game_engine


    def get_current_player(self) -> Player:
        return self._game_engine.get_current_player(self._states, self._players)

    def move(self):
        current_state = self.get_current_state()
        if self._game_engine.is_final_state(current_state):
            raise GameEnded("The game is over")
        current_player: Player = self.get_current_player()
        visible_states: List[State] = self._game_engine.get_visible_states(self._states, current_player)
        next_move: Play = current_player.play(visible_states)
        actual_state: State = self._states[-1]
        new_state: State = self._game_engine.update_state(actual_state, next_move)
        self._states.append(new_state)

    def get_players(self):
        return self._players
    
    def get_current_state(self):
        return self._states[-1]
    
    @property
    def states(self):
        return self._states


class Game(ABC):
    @staticmethod
    @abstractmethod
    def get_match(players: List[Player]) -> Match:
        pass
    
    @staticmethod
    @abstractmethod
    def get_visible_states(states: List[State], player: Player) -> List[State]:
        pass

    @staticmethod
    @abstractmethod
    def get_current_player(states: List[State], players: List[Player]) -> Player:
        pass
    
    @staticmethod
    @abstractmethod
    def update_state(actual_state: State, play: Play) -> State:
        pass
    
    @staticmethod
    @abstractmethod
    def is_final_state(state: State) -> bool:
        pass
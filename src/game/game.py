from typing import List
from abc import ABC, abstractmethod
from collections import namedtuple
from .state import State
from .player import Player, Play


class Match:
    def __init__(self, game_engine, players: List[Player]):
        self._states: List[State] = []
        self._players: List[Player] = players
        self._game_engine: Game = game_engine


    def get_current_player(self) -> Player:
        return self._game_engine.get_current_player(self._states, self._players)

    def move(self):
        current_player: Player = self.get_current_player()
        visible_states: List[State] = self._game_engine.get_visible_states(self._states, current_player)
        next_move: Play = current_player.play(self._states)
        actual_state: State = self._states[-1]
        new_state: State = self._game_engine.update_state(actual_state, next_move)
        self._states.append(new_state)

    def get_players(self):
        return self._players


class Game(ABC):
    @abstractmethod
    @staticmethod
    def get_match() -> Match:
        pass
    
    @abstractmethod
    @staticmethod
    def get_visible_states(states: List[State], player: Player) -> List[State]:
        pass

    @abstractmethod
    @staticmethod
    def get_current_player(states: List[State], players: List[Player]) -> Player:
        pass
    
    @abstractmethod
    @staticmethod
    def update_state(actual_state: State, play: Play) -> State:
        pass

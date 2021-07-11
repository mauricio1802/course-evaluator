from typing import List, NamedTuple
from .state import State
from abc import ABC, abstractmethod
from collections import namedtuple

PlayPayload = NamedTuple


class Play(NamedTuple):
    name: str
    payload: PlayPayload


class Player(ABC):
    @abstractmethod
    def play(self, states: List[State]) -> Play:
        pass
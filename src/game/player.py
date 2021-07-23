from typing import List, NamedTuple, NewType
from .state import State
from abc import ABC, abstractmethod, abstractproperty
from collections import namedtuple

PlayPayload = NamedTuple

Id = NewType('Id', int)

class Play(NamedTuple):
    name: str
    payload: PlayPayload


class Player(ABC):
    @abstractmethod
    def play(self, states: List[State]) -> Play:
        pass
    
    @abstractmethod
    def get_id(self) -> Id:
        pass

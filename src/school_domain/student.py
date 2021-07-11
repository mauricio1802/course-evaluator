from .fuzzy_system_var_interest import MockInterest

class Student:
    def __init__(
        self,
        energy: int,
        base_interest: float,
        hability: int
    ):
        self._energy: int = energy
        self._base_interest: float = base_interest
        self._hability: int = hability

    @property
    def energy(self) -> int:
        return self._energy

    @property
    def variable_interest(self) -> float:
        return MockInterest.get_variable_interest()
    
    @property
    def base_interest(self) -> float:
        return self._base_interest
    
    @property
    def interest(self) -> float:
        return min(1, self.variable_interest + self._base_interest)
    
    @property
    def hability(self) -> int:
        return self._hability
class Test:
    def __init__(self, interest_required: float, cost: int):
        self._interest_required: float = interest_required
        self._cost: int = cost
    
    @property
    def interest_required(self) -> float:
        return self._interest_required
    
    @property
    def cost(self) -> int:
        return self._cost
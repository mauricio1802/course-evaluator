from .fuzzy_logic import FuzzySet

class LinguisticVar:
    def __init__(self, name, terms, membership_functions, universe):
        assert len(terms) == len(membership_functions)
        self.name = name
        self.terms = dict(zip(terms, membership_functions))
        self.universe = universe
    
    def __getattr__(self, attr):
        return FuzzySet(self.universe, self.terms[attr])



class FuzzyFormula:
    def __init__(self):
        raise NotImplementedError
    
    def __call__(self, *vars_values):
        raise NotImplementedError
    
    def __or__(self, other):
        return Or(self, other)
    
    def __and__(self, other):
        return And(self, other)
    
    def __inverse__(self):
        return Not(self)
    
    def __rshift__(self, other):
        return FuzzyRule(self, other)
    
    def dimensions(self):
        raise NotImplementedError
    
    def domain(self):
        raise NotImplementedError


class Or(FuzzyFormula):
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    
    def __call__(self, *vars_values):
        f1_vars, f2_vars = vars_values[:self.f1.dimensions()], vars_values[-self.f2.dimensions():]
        return max(self.f1(*f1_vars), self.f2(*f2_vars))
    
    def dimensions(self):
        return self.f1.dimensions() + self.f2.dimensions()
    
    def domain(self):
        return self.f1.domain().union(self.f2.domain())


class And(FuzzyFormula):
    def __init__(self, f1, f2):
        self.f1 = f1
        self.f2 = f2
    
    def __call__(self, *vars_values):
        f1_vars, f2_vars = vars_values[:self.f1.dimensions()], vars_values[-self.f2.dimensions():]
        return min(self.f1(*f1_vars), self.f2(*f2_vars))
    
    def dimensions(self):
        return self.f1.dimensions() + self.f2.dimensions()
    
    def domain(self):
        return self.f1.domain().intersection(self.f2.domain())


class Not(FuzzyFormula):
    def __init__(self, f):
        self.f = f
    
    def __call__(self, *vars_values):
        return 1 - self.f(*vars_values)
    
    def dimensions(self):
        return self.dimensions()
    
    def domain(self):
        return self.f.domain()


class TruthValue(FuzzyFormula):
    def __init__(self, value):
        self.value = value

    def __call__(self):
        return self.value
    
    def dimensions(self):
        return 0


class FuzzySet(FuzzyFormula):
    def __init__(self, xs, membership_func):
        self._domain = set(xs)
        self.membership_func = membership_func
    
    def __call__(self, *vars_values):
        return self.membership_func(vars_values[0])

    def dimensions(self):
        return 1
    
    def domain(self):
        return self._domain


class FuzzyRule:
    def __init__(self, antecedent, consecuents):
        self.antecedent = antecedent
        self.consecuents = consecuents if isinstance(consecuents, tuple) else (consecuents, )
    

    



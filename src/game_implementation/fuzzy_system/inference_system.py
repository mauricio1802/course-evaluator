from itertools import accumulate
from collections import defaultdict
from src.fuzzy_logic import FuzzySet
from src.utils import plot_fuzzy_set

MANDAMI = "mandami"
LARSEN = "larsen"

class SystemRule:
    def __init__(self, *args):
        assert len(args) is 3 
        
        self.in_vars = args[0]
        self.out_vars = args[1]
        self.rule = args[2] 


class FuzzySystem:
    def __init__(self, var_input, var_output):
        self.var_input = var_input
        self.var_output = var_output
        self.rules = []
    
    def __iadd__(self, other):
        rule = SystemRule(*other)
        self.rules.append(rule)
        return self
    
    def __mandami_inference(self, *var_values):
        outputs = defaultdict(list)
        for rule in self.rules:
            values = [ value for (name, value) in var_values if name in rule.in_vars ]
            matching_degree = rule.rule.antecedent(*values)
            for i, consecuent in enumerate(rule.rule.consecuents):
                computed_set = FuzzySet(consecuent.domain(), lambda value, md = matching_degree, c = consecuent : min(md, c(value)))
                outputs[self.var_output[i]].append(computed_set)
        
        aggregate = lambda s : list(accumulate(s, lambda x, y : x | y))[-1]
        return {var : aggregate(s) for var, s in outputs.items()}

    def __larsen_inference(self, *var_values):
        outputs = defaultdict(list)
        for rule in self.rules:
            values = [ value for (name, value) in var_values if name in rule.in_vars ]
            matching_degree = rule.rule.antecedent(*values)
            for i, consecuent in enumerate(rule.rule.consecuents):
                computed_set = FuzzySet(consecuent.domain(), lambda value, md = matching_degree, c = consecuent : md * c(value))
                outputs[self.var_output[i]].append(computed_set)
        
        aggregate = lambda s : list(accumulate(s, lambda x, y : x | y))[-1]
        return {var : aggregate(s) for var, s in outputs.items()}

    def inference(self, *var_values, method = MANDAMI):
        var_values = zip(self.var_input, var_values)
        if method is MANDAMI:
            return self.__mandami_inference(*var_values)
        if method is LARSEN:
            return self.__larsen_inference(*var_values)


    

from random import random
from random import normalvariate
from numpy import arange
from .fuzzy_system import LinguisticVar, FuzzySystem, create_triangular, create_s, mom


class MockInterest:
    @staticmethod
    def get_variable_interest() -> float:
        return max(0, normalvariate(0.2, 0.2))


stress = LinguisticVar("Stress"
                    , ["stressed", "regular", "relaxed"]
                    , [ lambda value: 1 - create_s(0, 5)(value), create_triangular(3, 6, 8), create_s(5, 10) ]
                    , universe=arange(0, 10.1, 0.1))

mood = LinguisticVar("Mood"
                    , ["sad", "regular", "happy"]
                    , [ lambda value: 1 - create_s(0, 5)(value), create_triangular(3, 6, 8), create_s(5, 10) ]
                    , universe=arange(0, 10.1, 0.1))

health = LinguisticVar("Health"
                    , ["very_sick", "sick", "healthy"]
                    , [ lambda value: 1 - create_s(0, 5)(value), create_triangular(3, 6, 8), create_s(5, 10) ]
                    , universe=arange(0, 10.1, 0.1))

interest = LinguisticVar("Interest"
                        , ["uninterested", "interested", "very_interested"]
                        , [ lambda value: 1 - create_s(0, 5)(value), create_triangular(3, 6, 8), create_s(5, 10) ]
                        , universe=arange(0, 10.1, 0.1))

interest_calculator = FuzzySystem([stress, mood, health], [interest])

interest_calculator += (health, ), (interest, ), \
    (health.very_sick) >> interest.uninterested

interest_calculator += (stress, ), (interest, ), \
                    (stress.stressed) >> interest.uninterested

interest_calculator += (mood, health), (interest, ), \
    (mood.sad & health.sick) >> interest.uninterested

interest_calculator += (mood, health), (interest, ), \
    (mood.sad & health.healthy) >> interest.interested

interest_calculator += (stress, mood, health), (interest, ), \
    (stress.regular & mood.regular &
    (health.sick | health.healthy)) >> interest.interested

interest_calculator += (stress, mood, health), (interest, ), \
    (stress.regular & mood.happy & health.healthy) >> interest.very_interested

interest_calculator += (mood, health), (interest, ), \
                    (mood.happy & health.healthy) >> interest.very_interested

interest_calculator += (stress, mood, health), (interest, ), \
                    (stress.relaxed & mood.happy &
                        health.healthy) >> interest.interested


def generate_var_interest():
    s = min(10, max(normalvariate(5, 5), 0))
    m = min(10, max(normalvariate(5, 5), 0))
    h = min(10, max(normalvariate(5, 5), 0))
    var_interest = mom(interest_calculator.inference(s, m, h)[interest])
    return var_interest / 10
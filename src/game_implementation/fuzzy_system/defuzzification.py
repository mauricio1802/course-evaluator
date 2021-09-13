from numpy import mean
from scipy.integrate import quad
import matplotlib.pyplot as plt
from numpy import arange

EPSILON = 1e-6

def get_maximuns(f_set):
    maxi = 0
    maximuns = []
    for x in f_set.domain():
        if f_set(x) > maxi:
            maxi = f_set(x)
            maximuns = [x]
        elif f_set(x) == maxi:
            maximuns.append(x)
    return maximuns


def som(f_set):
    return sorted(get_maximuns(f_set))[0]


def lom(f_set):
    return sorted(get_maximuns(f_set))[-1]


def mom(f_set):
    return mean(get_maximuns(f_set))

def coa(f_set):
    dividend = 0
    divider = 0
    for x in f_set.domain():
        dividend += x * f_set(x)
        divider += f_set(x)
    return dividend / divider


def boa(f_set):
    ordered_domain = sorted(f_set.domain())
    fst, lst = ordered_domain[0], ordered_domain[-1]
    ans = fst
    dist = (lst - fst) / 2
    while True:
        inter1, _ = quad(f_set, fst, ans + dist)
        inter2, _ = quad(f_set, ans + dist, lst)

        if abs(inter1 - inter2) <= EPSILON:
            return ans
        if inter1 < inter2:
            ans += dist
            continue
        if inter1 > inter2:
            dist /= 2
            continue

import matplotlib.pyplot as plt


def plot_fuzzy_set(f_set):
    x = sorted(list(f_set.domain()))
    y = list(map(lambda x : f_set(x), x))
    plt.figure()
    plt.plot(x, y)
    plt.show()
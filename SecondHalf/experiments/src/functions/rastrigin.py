import math
def rastrigin(x, a=10):
    '''
    Rastrigin function: Notated as F4 in the paper(On benchmarking functions for genetic algorithm).

    x: A list of numbers.
    len(x): SHOULD be 20.
    x_i in x: SHOULD be in [-5.12, 5.12].
    '''
    value = 0
    for i in range(len(x)):
        value += x[i]**2 - 10*math.cos(2*math.pi*x[i]) + a
    return [value]

import math
def griewangk(x):
    '''
    Griewangk function: Notated as F8 in the paper(On benchmarking functions for genetic algorithm).

    x: A list of numbers.
    len(x): SHOULD be 10.
    x_i in x: SHOULD be in [-600, 600].
    '''
    value = 1
    for i in range(len(x)):
        value += x[i]**2/4000
    temp = 1
    for i in range(len(x)):
        temp *= math.cos(x[i]/math.sqrt(i+1))
    value -= temp
    return [value]

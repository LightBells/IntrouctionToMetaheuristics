import math
def schwefel(x):
    '''
    Schwefel function: Notated as F6 in the paper(On benchmarking functions for genetic algorithm).

    x: A list of numbers.
    len(x): SHOULD be 10.
    x_i in x: SHOULD be in [-500, 500].
    '''
    value = 418.9829*len(x) - sum([x[i]*math.sin(math.sqrt(abs(x[i]))) for i in range(len(x))])
    return [value]

def rosenbrock(x):
    '''
    Rosenbrock function: Notated as F2 in the paper(On benchmarking functions for genetic algorithm).
    x: A list of numbers.
    len(x): SHOULD be 2.
    x_i in x: SHOULD be in [-2.048, 2.048].
    '''
    value = 100*(x[1] - x[0]**2)**2 + (x[0] - 1)**2
    return [value]

def rosenbrock(x):
    '''
    Rosenbrock function: Notated as F2 in the paper(On benchmarking functions for genetic algorithm).
    x: A list of numbers.
    len(x): SHOULD be 2.
    x_i in x: SHOULD be in [-2048, 2048].
    '''
    value = 0
    for i in range(len(x)-1):
        value += 100*(x[i+1] - x[i]**2)**2 + (x[i] - 1)**2
    return [value]

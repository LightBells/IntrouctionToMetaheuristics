def sphere(x):
    '''
    Sphere function: Notated as F1 in the paper(On benchmarking functions for genetic algorithm).

    x: A list of numbers.
    len(x): SHOULD be 2.
    x_i in x: SHOULD be in [-5.12, 5.12].
    '''
    value = x[0]**2 + x[1]**2
    return [value]

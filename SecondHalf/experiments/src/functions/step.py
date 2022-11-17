def step(x):
    '''
    Step function: Notated as F3 in the paper(On benchmarking functions for genetic algorithm).

    x: A list of numbers.
    len(x): SHOULD be 5.
    x_i in x: SHOULD be in [-512, 512].
    '''
    value = 0
    for i in range(len(x)):
        value += int(x[i] > 0)
    return [value]

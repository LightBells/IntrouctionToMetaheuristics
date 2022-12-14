def foxholes(x, a):
    '''
    Foxholes function: Notated as F4 in the paper(On benchmarking functions for genetic algorithm).

    x: A list of numbers.
    len(x): SHOULD be 2.
    x_i in x: SHOULD be in [-65.536, 65.536].
    '''
    value = 0.002
    for j in range(25):
        temp = j + 1
        for i in range(2):
            temp += (x[i] - a[i][j])**6
        value += 1/temp
    return [1/value]

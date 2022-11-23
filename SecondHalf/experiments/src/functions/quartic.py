import random
def quartic(x):
    value = 0.0
    for i in range(len(x)):
        value += (i+1)*x[i]**4
    value += random.gauss(0, 1)
    return [value]

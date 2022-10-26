# アニーリング
from simanneal import Annealer
import urllib.request
import time
import psutil
url = 'https://raw.githubusercontent.com/maskot1977/ipython_notebook/master/toydata/location.txt'
urllib.request.urlretrieve(url, 'location.txt') # データのダウンロード

import pandas as pd
japan = pd.read_csv('location.txt')

# print(japan)


class TravellingSalesmanProblem(Annealer):

    """Test annealer with a travelling salesman problem.
    """

    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TravellingSalesmanProblem, self).__init__(state)  # important!

    def move(self):
        """Swaps two cities in the route."""
        # no efficiency gain, just proof of concept
        # demonstrates returning the delta energy (optional)
        initial_energy = self.energy()

        a = random.randint(0, len(self.state) - 1)
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

        return self.energy() - initial_energy

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i-1]][self.state[i]]


        e += self.distance_matrix[self.state[len(self.state)-1]][self.state[0]]
        return e

import numpy as np
from scipy.spatial import distance

mat = japan[['Latitude', 'Longitude']].values
dist_mat = distance.cdist(mat, mat, metric='euclidean') # ユークリッド距離

distance_matrix = {}
for i, town in enumerate(japan['Town']):
    if town not in distance_matrix.keys():
        distance_matrix[town] = {}
    for j, town2 in enumerate(japan['Town']):
        distance_matrix[town][town2] = dist_mat[i][j]


# print(distance_matrix)
# print()
# print(list(distance_matrix.keys()))
# print(list(distance_matrix.keys())[5])
# print()


import random
init_state = list(japan['Town'])
random.shuffle(init_state)

avg = 0
avg_memory = 0
avg_time = 0

max = 100000
min = 0

for t in range(10):

    tsp = TravellingSalesmanProblem(init_state, distance_matrix)

    b1 = psutil.virtual_memory()
    start = time.time()
    tsp.set_schedule(tsp.auto(minutes=0.2))
    tsp.copy_strategy = "slice"
    state, e = tsp.anneal()
    end = time.time()
    b2 = psutil.virtual_memory()


    # print(e)
    # print(state)


    # while state[0] != 'Sapporo':
            # state = state[1:] + state[:1]  # rotate NYC to start

    # print()
    # print()
    # print("distance : ",e)
    # print('the time cost : ',end - start )
    # print("memory used : ",abs((b1.used - b2.used)/1000/1000)," GB")
    # print()

    avg += e
    avg_time += end - start
    avg_memory += abs((b1.used - b2.used)/1000/1000)

    if e < max:
        max = e
        import matplotlib.pyplot as plt

        fig = plt.figure(figsize=(10, 10))
        Xs = []
        Ys = []
        for i in range(len(state)):
            Xs.append(list(japan[japan['Town'] == state[i]].iloc[:, 2])[0])
            Ys.append(list(japan[japan['Town'] == state[i]].iloc[:, 1])[0])

        plt.plot(Xs, Ys)
        for city, x, y in zip(japan['Town'], japan['Latitude'], japan['Longitude']):
            plt.text(x, y, city, alpha=0.5, size=12)
        plt.grid()
        # plt.show()
        fig.savefig("tsp_annerling.png")
    if e > min:
        min = e

    # print(state)

    # print(list(japan[japan['Town'] == state[5]].iloc[:, 0])[0])
    # print()
    # print(list( distance_matrix.keys())[5] )

print()
print("avg distance : ",avg/10)
print('avg the time cost : ',avg_time/10 )
print("memory used : ",avg_memory/10," MB")
print()

print("max distance : ", max)
print("min distance : ",min)
print()
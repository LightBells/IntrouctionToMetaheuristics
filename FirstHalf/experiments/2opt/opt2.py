# 2-opt
from itertools import combinations
import os,sys,copy
import numpy as np
import pandas as pd
from scipy.spatial import distance
import time
import random
from pathlib import Path
from typing import (
    Optional,
    Dict,
    Tuple,
    List,
)
import urllib.request
from memory_profiler import profile
import matplotlib.pyplot as plt

def download_file(url: str, path: Path) -> Optional[Path]:
    """Download a file from a URL to a given path."""
    if not path.exists():
        # Create the directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # データのダウンロード
        urllib.request.urlretrieve(url, path)
    except Exception as e:
        print(e)
        return None

    return path

def load_distance_matrix(path: Path) -> Tuple[Dict[int, str], List[List[float]]]:
    """Load a distance matrix from a given path."""
    japan = pd.read_csv(path)
    mat = japan[['Latitude', 'Longitude']].values
    # ユークリッド距離
    dist_mat = distance.cdist(mat, mat, metric='euclidean')
    int2town = {i: v for i, v in enumerate(japan['Town'])}
    return int2town, dist_mat


class Opt2():
    def __init__(self,disMatrix,max_iters=100,max_no_improvement=10):
        """parameters definition"""
        self.disMatrix = disMatrix
        self.max_no_improvement = max_no_improvement
        self.max_iters = max_iters
        
    def cost(self, solution):
        cost = 0
        for i in range(1, len(solution)):
            cost += self.disMatrix[solution[i-1]][solution[i]]
        cost += self.disMatrix[solution[-1]][solution[0]]
        return cost
        
    def get_initial_solution(self):
        init = list(range(len(self.disMatrix)))
        random.shuffle(init)
        return init

    def opt2_search(self,solution):
        size = len(solution)
        while True:
            count = 0
            for i in range(size - 2):
                i1 = i + 1
                for j in range(i + 2, size):
                    if j == size - 1:
                        j1 = 0
                    else:
                        j1 = j + 1
                    if i != 0 or j1 != 0:
                        l1 = self.disMatrix[solution[i]][solution[i1]]
                        l2 = self.disMatrix[solution[j]][solution[j1]]
                        l3 = self.disMatrix[solution[i]][solution[j]]
                        l4 = self.disMatrix[solution[i1]][solution[j1]]
                    if l1 + l2 > l3 + l4:
                        new_solution = solution[i1:j+1]
                        solution[i1:j+1] = new_solution[::-1]
                        count += 1
            if count == 0:
                break
        return solution


if __name__ == "__main__":
    url = 'https://raw.githubusercontent.com/maskot1977/ipython_notebook/master/toydata/location.txt'
    path = Path('data') / 'location.txt'

    path = download_file(url, path)
    if path is None:
        print('Download failed.', file=sys.stderr)
        exit(1)
    
    towns, distance_matrix = load_distance_matrix(path)
    
    tsp = Opt2(disMatrix=distance_matrix ,max_iters=10000,max_no_improvement=300)

    best_cost = 1e10
    worst_cost = 0
    avg_cost = 0

    avg_time = 0

    best_tour: List[int] = []
    worst_tour: List[int] = []
    
    @profile
    def solve():
        return tsp.opt2_search(tsp.get_initial_solution())

    for i in range(10):
        # Solve the problem
        start = time.time()
        tour = solve()
        end = time.time()

        cost = tsp.cost(tour)
        avg_cost += cost
        avg_time += end - start

        if cost < best_cost:
            best_cost = cost
            best_tour = tour

        if cost > worst_cost:
            worst_tour = tour
            worst_cost = cost

    # Rotate the tour so that it starts from the first town
    best_tour = best_tour[best_tour.index(0):] + best_tour[:best_tour.index(0)]
    worst_tour = worst_tour[worst_tour.index(0):] + worst_tour[:worst_tour.index(0)]

    # Print the best tour and its cost
    print('Best tour: {}'.format([*map(lambda x:towns[x], best_tour)]))
    print('Worst tour: {}'.format([*map(lambda x:towns[x], worst_tour)]))

    print('Best cost: {}'.format(tsp.cost(best_tour)))
    print('Worst cost: {}'.format(tsp.cost(worst_tour)))

    print('Average cost: {}'.format(avg_cost/10))
    print('Average time: {}s'.format(avg_time/10))
    

    fig = plt.figure(figsize=(10, 10))
    japan = pd.read_csv('location.txt')
    mat = japan[['Latitude', 'Longitude']].values
    dist_mat = distance.cdist(mat, mat, metric='euclidean')
    distance_matrix = {}
    for i, town in enumerate(japan['Town']):
        if town not in distance_matrix.keys():
            distance_matrix[town] = {}
        for j, town2 in enumerate(japan['Town']):
            distance_matrix[town][town2] = dist_mat[i][j]
    Xs = []
    Ys = []
    for i in range(len(best_tour)):
        Xs.append(list(japan[japan['Town'] == list( distance_matrix.keys())[i]].iloc[:, 2])[0])
        Ys.append(list(japan[japan['Town'] == list( distance_matrix.keys())[i]].iloc[:, 1])[0])
    plt.plot(Xs, Ys)
    for city, x, y in zip(japan['Town'], japan['Latitude'], japan['Longitude']):
        plt.text(x, y, city, alpha=0.5, size=12)
    plt.grid()
    plt.show()
    fig.savefig("opt2_best.png")

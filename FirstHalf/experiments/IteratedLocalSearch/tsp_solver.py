import urllib.request
import pandas as pd
import numpy as np
from scipy.spatial import distance
import random
from pathlib import Path
from typing import (
        Optional,
        Dict,
        Tuple,
        List,
    )
import sys
from tsp_by_ils import TSP, TSP_ILS
import time
from memory_profiler import profile


def download_file(url: str, path: Path) -> Optional[Path]:
    """Download a file from a URL to a given path.
    """
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


def load_distance_matrix(path: Path) -> Tuple[
        Dict[int, str], List[List[float]]
        ]:
    """Load a distance matrix from a given path.
    """
    japan = pd.read_csv(path)
    mat = japan[['Latitude', 'Longitude']].values
    # ユークリッド距離
    dist_mat = distance.cdist(mat, mat, metric='euclidean')
    int2town = {i: v for i, v in enumerate(japan['Town'])}
    return int2town, dist_mat


def main() -> None:
    url = 'https://raw.githubusercontent.com/maskot1977/'\
                'ipython_notebook/master/toydata/location.txt'
    path = Path('data') / 'location.txt'

    path = download_file(url, path)
    if path is None:
        print('Download failed.', file=sys.stderr)
        exit(1)

    towns, distance_matrix = load_distance_matrix(path)
  
    # Initialize the problem
    tsp = TSP(distance_matrix)

    # Initialize the solver
    solver = TSP_ILS(tsp, max_iterations=10000, max_no_improvement=300)

    best_cost = 1e10
    worst_cost = 0
    avg_cost = 0

    avg_time = 0

    best_tour: List[int] = []
    worst_tour: List[int] = []

    # @profile
    def solve():
        return solver.search(tsp.get_initial_solution())

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


if __name__ == '__main__':
    main()

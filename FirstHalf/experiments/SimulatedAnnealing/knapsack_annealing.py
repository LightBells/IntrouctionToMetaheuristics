# Title: KnapSack Simulated Annealing
# Author: Hikaru Takanashi
# Date: 2022/10/26
import urllib.request
from pathlib import Path
from typing import (
        Optional,
        Dict,
        List,
    )
import sys
import time
from memory_profiler import profile
from simanneal import Annealer
import random


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


class KnapSack_SA(Annealer):
    def __init__(self, capacity, weights, values):
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.n = len(weights)
        state = self.get_initial_solution()
        super(KnapSack_SA, self).__init__(state)

    def move(self):
        """Swaps two cities in the route."""
        initial_energy = self.energy()

        # indexをランダムに選択
        idx = random.randint(0, len(self.state)-1)
        if self.state[idx] == 0:
            self.state[idx] = 1
        else:
            self.state[idx] = 0

        while not self.is_valid():
            self.state[idx] = 0
            idx = random.randint(0, len(self.state)-1)
            if self.state[idx] == 0:
                self.state[idx] = 1
            else:
                self.state[idx] = 0

        return self.energy() - initial_energy

    def is_valid(self, canditate=None):
        """ Checks if the current state is valid.
        """
        if canditate is not None:
            s = canditate
        else:
            s = self.state

        weights = [w*i for w, i in zip(self.weights, s)]
        return sum(weights) <= self.capacity

    def energy(self):
        """Calculates the length of the route."""
        e = sum([v*i for v, i in zip(self.values, self.state)])
        return -e

    def get_initial_solution(self):
        canditate = [random.randint(0, 1) for i in range(self.n)]
        while not self.is_valid(canditate=canditate):
            canditate = [random.randint(0, 1) for i in range(self.n)]
        return canditate

def main() -> None:
    """Main function.
    """

    # Data is obtained from 
    # https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/knapsack_01.html
    urls = {
        "capacity": "https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p08_c.txt",
        "weights": "https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p08_w.txt",
        "values": "https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/p08_p.txt"
    }
    data_path = Path('data')

    results = [download_file(url, data_path / (name+".txt")) for name, url in urls.items()]
    for result in results:
        if result is None:
            print('Download failed.', file=sys.stderr)
            exit(1)

    # Read the data
    capacity = int(open(data_path / "capacity.txt").read())

    weights = []
    with open(data_path / "weights.txt") as f:
        for line in f:
            weights.append(int(line))

    values = []
    with open(data_path / "values.txt") as f:
        for line in f:
            values.append(int(line))

    worst_value = 1e10
    best_value = 0
    avg_value = 0

    avg_time = 0

    for i in range(10):
        ks = KnapSack_SA(capacity=capacity, weights=weights, values=values)
        ks.set_schedule(ks.auto(minutes=0.2))
        ks.copy_strategy = "slice"

        # @profile
        def solve():
            return ks.anneal()

        # Solve the problem
        start = time.time()
        state, e = solve()
        end = time.time()

        value = -e
        avg_value += value
        avg_time += end - start

        if best_value < value:
            best_value = value

        if worst_value > value:
            worst_value = value

    print("")
    print('Best value: {}'.format(best_value))
    print('Worst value: {}'.format(worst_value))

    print('Average value: {}'.format(avg_value/10))
    print('Average time: {}s'.format(avg_time/10))


if __name__ == '__main__':
    main()

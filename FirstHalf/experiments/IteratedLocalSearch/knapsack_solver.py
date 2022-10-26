import urllib.request
from pathlib import Path
from typing import (
        Optional,
        Dict,
        Tuple,
        List,
    )
import sys
from knapsack_by_ils import KnapSack, KnapSack_ILS
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
  
    # Initialize the problem
    knapsack = KnapSack(capacity, weights, values)

    # Initialize the solver
    solver = KnapSack_ILS(
            knapsack,
            max_iterations=10000,
            max_no_improvement=3000)

    worst_value = 1e10
    best_value = 0
    avg_value = 0

    avg_time = 0

    # @profile
    def solve():
        return solver.search(knapsack.get_initial_solution())

    for i in range(10):
        # Solve the problem
        start = time.time()
        solution = solve()
        end = time.time()

        value = -knapsack.cost(solution)
        avg_value += value
        avg_time += end - start

        if best_value < value:
            best_value = value

        if worst_value > value:
            worst_value = value

    print('Best value: {}'.format(best_value))
    print('Worst value: {}'.format(worst_value))

    print('Average value: {}'.format(avg_value/10))
    print('Average time: {}s'.format(avg_time/10))


if __name__ == '__main__':
    main()

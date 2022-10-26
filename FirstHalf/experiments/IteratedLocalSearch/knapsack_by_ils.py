from ILS import IteratedLocalSearch
from ILS import Problem
import random
import copy


class KnapSack(Problem):
    def __init__(self, capacity, weights, values):
        super().__init__(
                "KnapSack Problem",
                "A simple example of a knapsack problem")
        self.capacity = capacity
        self.weights = weights
        self.values = values
        self.n = len(weights)

    def cost(self, solution):
        cost = 0
        for i in range(len(solution)):
            cost += self.values[i] * solution[i]
        return -cost

    def is_valid(self, solution):
        current_weight = sum([w*s for w, s in zip(self.weights, solution)])
        return current_weight <= self.capacity

    def get_initial_solution(self):
        canditate = [random.randint(0, 1) for i in range(self.n)]
        while not self.is_valid(canditate):
            canditate = [random.randint(0, 1) for i in range(self.n)]
        return canditate


class KnapSack_ILS(IteratedLocalSearch):
    def __init__(self, problem, max_iterations=100, max_no_improvement=10):
        super().__init__(problem, max_iterations, max_no_improvement)

    def local_search(self, solution, p=0.8):
        while self.problem.is_valid(solution):
            prev_solution = copy.deepcopy(solution)
            idx = random.randint(0, self.problem.n-1)
            if solution[idx] == 0:
                solution[idx] = 1
            elif random.random() < p:
                solution[idx] = 0
        return prev_solution

    # Use random erase as the kick(perturbation) operator
    def perturbation(self, solution):
        num_erase = random.randint(1, self.problem.n//4)
        for i in range(num_erase):
            idx = random.randint(0, self.problem.n-1)
            while solution[idx] == 0:
                idx = random.randint(0, self.problem.n-1)
            solution[idx] = 0

        return solution



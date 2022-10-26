from GLS import GuidedLocalSearch
from GLS import Problem
import random


class TSP(Problem):
    def __init__(self, distance_matrix):
        super().__init__(
                "Traveling Salesman Problem",
                "A simple example of a TSP problem")
        self.distance_matrix = distance_matrix

    def cost(self, solution):
        cost = 0
        for i in range(1, len(solution)):
            cost += self.distance_matrix[solution[i-1]][solution[i]]
        cost += self.distance_matrix[solution[-1]][solution[0]]
        return cost

    def get_initial_solution(self):
        init = list(range(len(self.distance_matrix)))
        random.shuffle(init)
        return init


class TSP_GLS(GuidedLocalSearch):
    def __init__(self, problem, max_iterations=100, alpha=0.5):
        super().__init__(problem, max_iterations, alpha)

    def local_search(self, solution, lambda_):
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
                        l1 = self.problem.distance_matrix[solution[i]][solution[i1]] + lambda_ * self.penalty[solution[i]][solution[i1]]
                        l2 = self.problem.distance_matrix[solution[j]][solution[j1]] + lambda_ * self.penalty[solution[j]][solution[j1]]
                        l3 = self.problem.distance_matrix[solution[i]][solution[j]] + lambda_ * self.penalty[solution[i]][solution[j]]
                        l4 = self.problem.distance_matrix[solution[i1]][solution[j1]] + lambda_ * self.penalty[solution[i1]][solution[j1]]
                        if l1 + l2 > l3 + l4:
                            new_solution = solution[i1:j+1]
                            solution[i1:j+1] = new_solution[::-1]
                            count += 1
            if count == 0:
                break
        return solution

    def init_penalty(self):
        return [
                [0 for _ in range(len(self.problem.distance_matrix))]
                for _ in range(len(self.problem.distance_matrix))]

    def update_penalty(self, solution):
        max_util = 0
        max_idx = []

        for i in range(len(self.penalty)):
            for j in range(len(self.penalty)):
                if i != j:
                    util = self.utility(solution, (i, j))
                    if util > max_util:
                        max_util = util
                        max_idx = []
                        max_idx.append((i, j))
                    elif util == max_util:
                        max_idx.append((i, j))

        for idx in max_idx:
            self.penalty[idx[0]][idx[1]] += 1
            self.penalty[idx[1]][idx[0]] += 1


    def utility(self, solution, idx):
        idx1, idx2 = idx

        indicator = 0
        for i in range(len(solution)):
            if (solution[i] == idx1 and solution[(i+1) % len(solution)] == idx2):
                indicator = 1
                break
        util = indicator * self.problem.distance_matrix[idx1][idx2] / (1 + self.penalty[idx1][idx2])
        return util

    def lambda_calculation(self, g):
        return self.alpha * g / len(self.problem.distance_matrix)

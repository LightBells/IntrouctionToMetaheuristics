from ILS import IteratedLocalSearch
from ILS import Problem
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


class TSP_ILS(IteratedLocalSearch):
    def __init__(self, problem, max_iterations=100, max_no_improvement=10):
        super().__init__(problem, max_iterations, max_no_improvement)

    def local_search(self, solution):
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
                        l1 = self.problem.distance_matrix[solution[i]][solution[i1]]
                        l2 = self.problem.distance_matrix[solution[j]][solution[j1]]
                        l3 = self.problem.distance_matrix[solution[i]][solution[j]]
                        l4 = self.problem.distance_matrix[solution[i1]][solution[j1]]
                        if l1 + l2 > l3 + l4:
                            new_solution = solution[i1:j+1]
                            solution[i1:j+1] = new_solution[::-1]
                            count += 1
            if count == 0:
                break
        return solution

    # Use double bridge move as the kick(perturbation) operator
    def perturbation(self, solution):
        size = len(solution)
        pos1 = random.randint(1, size//4)
        pos2 = pos1+random.randint(1, size//4)
        pos3 = pos2+random.randint(1, size//4)

        perturbed_solution = []
        perturbed_solution.extend(solution[0:pos1])
        perturbed_solution.extend(solution[pos3:])
        perturbed_solution.extend(solution[pos2:pos3])
        perturbed_solution.extend(solution[pos1:pos2])
        return perturbed_solution

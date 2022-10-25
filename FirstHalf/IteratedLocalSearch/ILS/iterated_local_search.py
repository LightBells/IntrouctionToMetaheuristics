import abc


class IteratedLocalSearch(object, metaclass=abc.ABCMeta):
    def __init__(self, problem, max_iterations=100, max_no_improvement=10):
        self.problem = problem
        self.max_iterations = max_iterations
        self.max_no_improvement = max_no_improvement

    def search(self, init_solution):
        best = self.local_search(init_solution)
        best_cost = self.problem.cost(best)
        no_improvement = 0

        for i in range(self.max_iterations):
            seed_solution = best
            kicked_solution = self.perturbation(seed_solution)
            candidate = self.local_search(kicked_solution)
            candidate_cost = self.problem.cost(candidate)

            if candidate_cost < best_cost:
                best, best_cost = candidate, candidate_cost
                no_improvement = 0
            else:
                no_improvement += 1
            if no_improvement >= self.max_no_improvement:
                break
        return best

    @abc.abstractmethod
    def local_search(self, solution):
        pass

    @abc.abstractmethod
    def perturbation(self, solution):
        pass

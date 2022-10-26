import abc
import copy


class GuidedLocalSearch(object, metaclass=abc.ABCMeta):
    def __init__(self, problem, max_iterations=100, alpha=0.5):
        self.problem = problem
        self.max_iterations = max_iterations
        self.alpha = alpha

    def search(self, init_solution):
        solution = best_solution = init_solution
        self.penalty = self.init_penalty()

        for k in range(self.max_iterations):
            g = self.problem.cost(best_solution)
            lambda_ = self.lambda_calculation(g)
            solution = self.local_search(solution, lambda_)
            self.update_penalty(solution)
            if self.problem.cost(solution) < self.problem.cost(best_solution):
                best_solution = copy.deepcopy(solution)
        return best_solution

    @abc.abstractmethod
    def local_search(self, solution, lambda_):
        pass

    @abc.abstractmethod
    def init_penalty(self):
        pass

    @abc.abstractmethod
    def update_penalty(self, solution):
        pass

    @abc.abstractmethod
    def utility(self, solution, idx):
        pass

    @abc.abstractmethod
    def lambda_calculation(self, g):
        pass

import abc


class Problem(object, metaclass=abc.ABCMeta):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @abc.abstractmethod
    def cost(self, solution):
        pass

    @abc.abstractmethod
    def get_initial_solution(self):
        pass

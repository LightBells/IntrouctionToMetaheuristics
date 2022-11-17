# https://dse-souken.com/2021/05/25/ai-19/
import random

from deap import (
        base,
        creator,
        tools,
        algorithms
    )
from typing import Callable, Dict

class GeneticAlgorithm:
    def __init__(
            self,
            generations,
            population_size,
            crossover_probability,
            mutation_probability,
        ):
        self.NGEN = generations
        self.POPULATION_SIZE = population_size
        self.CXPB = crossover_probability
        self.MUTPB = mutation_probability

        creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
        self.creator = creator


    def solve(self, obj_fn: Callable, n: int, lb: float, ub: float, sigma:float, seed:int, verbose: bool = False) -> None:
        toolbox = base.Toolbox()
        toolbox.register("attribute", random.uniform, lb, ub)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=n)
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        toolbox.register("select", tools.selTournament, tournsize=5)
        toolbox.register("mate", tools.cxBlend, alpha=0.2)
        toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=sigma, indpb=0.2)
        toolbox.register("evaluate", obj_fn)

        random.seed(seed)


        pop = toolbox.population(n=self.POPULATION_SIZE)
        for individual in pop:
            individual.fitness.values = toolbox.evaluate(individual)

        hof = tools.ParetoFront()

        algorithms.eaSimple(
                pop, 
                toolbox, 
                cxpb=self.CXPB, 
                mutpb=self.MUTPB, 
                ngen=self.NGEN, 
                halloffame=hof,
                verbose = verbose)

        best_individual = tools.selBest(pop, k=1)[0]

        return best_individual, best_individual.fitness.values

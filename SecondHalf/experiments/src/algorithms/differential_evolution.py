from scipy.optimize import differential_evolution
import random

from typing import Callable, Dict

class DifferentialEvolution:
    def __init__(
            self,
            maxiter=1000, 
            tol=0.01, 
            init='latinhypercube', 
            updating='immediate', 
            popsize=15, 
            mutation=(0.5, 1), 
            recombination=0.7, 
            workers=1
        ):
        self.maxiter = maxiter
        self.tol = tol
        self.init = init
        self.updating = updating
        self.popsize = popsize
        self.mutation = mutation
        self.recombination = recombination
        self.workers = workers

    def solve(self, 
            obj_fn: Callable, 
            n: int, 
            lb: float, 
            ub: float,
            seed=None, 
            verbose=False, 
        ) -> None:
        result = differential_evolution(
            obj_fn,
            bounds=[(lb, ub)] * n,
            maxiter=self.maxiter,
            tol=self.tol,
            init=self.init,
            updating=self.updating,
            workers=self.workers,
            mutation=self.mutation,
            recombination=self.recombination,
            seed=seed,
            popsize=self.popsize,
            disp=verbose,
        )
        return result.x, result.fun


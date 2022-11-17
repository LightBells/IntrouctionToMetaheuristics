import numpy as np
import pyswarms as ps
from typing import Callable
import utils.functools as ft

class ParticleSwarmOptimization:
    def __init__(
            self,
            maxiter=1000, 
            num_particles=100,
            c1=0.5, 
            c2=0.3,
            w=0.9,
        ):
        self.maxiter = maxiter
        self.num_particles = num_particles
        self.options = {'c1': c1, 'c2': c2, 'w': w}

    def solve(self, 
            obj_fn: Callable, 
            n: int, 
            lb: float, 
            ub: float,
            seed=None, 
            verbose=False, 
        ) -> None:
        """Solve the optimization problem using Particle Swarm Optimization.
        """
        # To accept numpy arrays, we need to wrap the objective function
        unwrapped_obj_fn = ft.unwrap(obj_fn)
        def wrapped_obj_fn(x):
            return np.apply_along_axis(unwrapped_obj_fn, 1, x)

        np.random.seed(seed)
        bounds = ([lb]*n, [ub]*n)
        optimizer = ps.single.GlobalBestPSO(n_particles=self.num_particles, dimensions=n, options=self.options, bounds=bounds)

        cost, pos = optimizer.optimize(wrapped_obj_fn, iters=self.maxiter, verbose=verbose)
        return pos, cost

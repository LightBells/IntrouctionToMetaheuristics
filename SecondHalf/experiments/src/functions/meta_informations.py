from functions.sphere import sphere
from functions.rosenbrock import rosenbrock
from functions.step import step
from functions.quartic import quartic
from functions.foxholes import foxholes
from functions.schwefel import schwefel
from functions.rastrigin import rastrigin
from functions.griewangk import griewangk

meta_informations = [
    {
        "name": "sphere",
        "function": sphere,
        "dimension": 2,
        "lower_bound": -5.12,
        "upper_bound": 5.12,
        "optimal_value": 0,
        "optimal_solution": [0, 0],
    },
    {
        "name": "rosenbrock",
        "function": rosenbrock,
        "dimension": 2,
        "lower_bound": -2048,
        "upper_bound": 2048,
        "optimal_value": 0,
        "optimal_solution": [1, 1],
    },
    {
        "name": "step",
        "function": step,
        "dimension": 5,
        "lower_bound": -1,
        "upper_bound": 1,
        "optimal_value": 0,
        "optimal_solution": None,
    },
    {
        "name": "quartic",
        "function": quartic,
        "dimension": 30,
        "lower_bound": -1.28,
        "upper_bound": 1.28,
        "optimal_value": 0,
        "optimal_solution": [0]*30,
    },
    {
        "name": "foxholes",
        "function": foxholes,
        "dimension": 2,
        "lower_bound": -1,
        "upper_bound": 1,
        "optimal_value": 0.998003837794449325873406851315,
        "optimal_solution": [-31.97833]*2,
        "kwargs": {"a":[
            [-32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32, -32, -16, 0, 16, 32],
            [-32, -32, -32, -32, -32, -16, -16, -16, -16, -16, 0, 0, 0, 0, 0, 16, 16, 16, 16, 16, 32, 32, 32, 32, 32],
        ]},
    },
    {
        "name": "schwefel",
        "function": schwefel,
        "dimension": 10,
        "lower_bound": -500,
        "upper_bound": 500,
        "optimal_value": 0,
        "optimal_solution": [420.9687]*10,
    },
    {
        "name": "rastrigin",
        "function": rastrigin,
        "dimension": 20,
        "lower_bound": -5.12,
        "upper_bound": 5.12,
        "optimal_value": 0,
        "optimal_solution": [0]*20,
    },
    {
        "name": "griewangk",
        "function": griewangk,
        "dimension": 10,
        "lower_bound": -600,
        "upper_bound": 600,
        "optimal_value": 0,
        "optimal_solution": [0]*10,
    },
]

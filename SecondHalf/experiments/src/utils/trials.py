from typing import Dict
from algorithms import GeneticAlgorithm
from algorithms import DifferentialEvolution
from algorithms import ParticleSwarmOptimization
from functions.meta_informations import meta_informations
import utils.functools as ft
import time

def trials(configurations: Dict)->Dict:
    log = [];

    # Genetic Algorithm
    print(f"Running Genetic Algorithm")
    print("=========================================")
    for population in configurations["genetic_algorithm"]["canditate_populations"]:
        print("Population Size: {}".format(population))
        for cp in configurations["genetic_algorithm"]["canditate_crossover_rates"]:
            print("Crossover Probability: {}".format(cp))
            for mp in configurations["genetic_algorithm"]["canditate_mutation_rates"]:
                print("Mutation Probability: {}".format(mp))
                ga = GeneticAlgorithm(
                    generations=configurations["genetic_algorithm"]["generations"],
                    population_size=population,
                    crossover_probability=cp,
                    mutation_probability=mp,
                )
                
                for meta_information in meta_informations:
                    obj_fn = ft.get_partial_obj_fn(meta_information);

                    print(f"Running {meta_information['name']}...")
                    start = time.time()
                    best_solution, value = ga.solve(
                        obj_fn=obj_fn,
                        n=meta_information["dimension"],
                        lb=meta_information["lower_bound"],
                        ub=meta_information["upper_bound"],
                        sigma=0.1,
                        seed=configurations["seed"],
                        verbose=False,
                    )
                    end = time.time()

                    print("The best solution is: ", best_solution)
                    print("The value of the best solution is: ", value[0])
                    print("The optimal solution is: ", meta_information["optimal_solution"])
                    print("The optimal value is: ", meta_information["optimal_value"])
                    print("The time taken is: ", end - start)

                    log.append({
                        "algorithm": "genetic",
                        "function": meta_information["name"],
                        "population": population,
                        "crossover_probability": cp,
                        "mutation_probability": mp,
                        "best_solution": best_solution,
                        "value": value[0],
                        "time": end - start,
                    })

    # Differential Evolution
    print(f"Running Differential Evolution")
    print("=========================================")
    for population in configurations["differential_evolution"]["canditate_populations"]:
        for mutation in configurations["differential_evolution"]["canditate_mutation_rates"]:
            for recombination in configurations["differential_evolution"]["canditate_recombination_rates"]:
                differential_evolution = DifferentialEvolution(
                    maxiter=configurations["differential_evolution"]["maxiter"],
                    popsize=population,
                    mutation=mutation,
                    recombination=recombination,
                    workers=4,
                )

                for meta_information in meta_informations:
                    print(f"Running {meta_information['name']} with Differential Evolution")
                    obj_fn = ft.get_partial_obj_fn(meta_information)
                    start = time.time()
                    best_solution, value = differential_evolution.solve(
                        obj_fn = obj_fn,
                        n = meta_information["dimension"],
                        lb = meta_information["lower_bound"],
                        ub = meta_information["upper_bound"],
                        seed = configurations["seed"],
                        verbose = False,
                    )
                    end = time.time()

                    print("The best solution is: ", best_solution)
                    print("The value of the best solution is: ", value)
                    print("The optimal solution is: ", meta_information["optimal_solution"])
                    print("The optimal value is: ", meta_information["optimal_value"])
                    print("The time taken is: ", end - start)

                    log.append({
                        "algorithm": "differential_evolution",
                        "function": meta_information["name"],
                        "population": population,
                        "mutation_probability": mutation,
                        "recombination": recombination,
                        "best_solution": best_solution,
                        "value": value,
                        "time": end - start,
                    })


    # Particle Swarm Optimization
    print(f"Running Particle Swarm Optimization")
    print("=========================================")
    for population in configurations["particle_swarm_optimization"]["canditate_populations"]:
        for c1 in configurations["particle_swarm_optimization"]["canditate_c1"]:
            for c2 in configurations["particle_swarm_optimization"]["canditate_c2"]:
                for w in configurations["particle_swarm_optimization"]["canditate_w"]:
                    particle_swarm_optimization = ParticleSwarmOptimization(
                        maxiter=configurations["particle_swarm_optimization"]["maxiter"],
                        num_particles=population,
                        c1=c1,
                        c2=c2,
                        w=w
                    )

                    for meta_information in meta_informations:
                        print(f"Running {meta_information['name']} with Particle Swarm Optimization")
                        obj_fn = ft.get_partial_obj_fn(meta_information)
                        start_time = time.time()
                        best_solution, value = particle_swarm_optimization.solve(
                            obj_fn = obj_fn,
                            n = meta_information["dimension"],
                            lb = meta_information["lower_bound"],
                            ub = meta_information["upper_bound"],
                            seed = configurations["seed"],
                            verbose = False,
                        )
                        end_time = time.time()

                        print("The best solution is: ", best_solution)
                        print("The value of the best solution is: ", value)
                        print("The optimal solution is: ", meta_information["optimal_solution"])
                        print("The optimal value is: ", meta_information["optimal_value"])
                        print("The time taken is: ", end_time - start_time)

                        log.append({
                            "algorithm": "particle_swarm_optimization",
                            "function": meta_information["name"],
                            "population": population,
                            "c1": c1,
                            "c2": c2,
                            "w": w,
                            "best_solution": best_solution,
                            "value": value,
                            "time": end_time - start_time,
                        })


    return log


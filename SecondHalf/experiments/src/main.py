from utils import trials
from utils import CSVExporter

def main() -> None:
    print("Starting Trials")
    print("=========================================")

    iteratations = 10
    configurations = {
       "differential_evolution": {
           "maxiter": 1000,
           "canditate_populations": [10, 20, 50, 100, 200, 500, 800, 1000],
           "canditate_recombination_rates": [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95],
           "canditate_mutation_rates": [0.001, 0.02, 0.04, 0.06, 0.08, 0.10, 0.18, 0.20],
       },
       "genetic_algorithm": {
           "generations": 100,
           "canditate_populations": [10, 20, 50, 100, 200, 500, 800, 1000],
           "canditate_crossover_rates": [0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95],
           "canditate_mutation_rates": [0.001, 0.02, 0.04, 0.06, 0.08, 0.10, 0.18, 0.20],
       },
       "particle_swarm_optimization": {
               "canditate_populations": [10, 20, 50, 100, 200, 500, 800, 1000],
               "canditate_c1": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
               "canditate_c2": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
               "canditate_w": [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
               "maxiter": 1000,
       },
       "seed": 1234,
    }

    logs = trials(iteratations, configurations)

    print("=========================================")
    print("Writing Logs...")
    CSVExporter.export("result/result.csv", logs)

    print("=========================================")
    print("Finished Trials")

if __name__ == "__main__":
    main()

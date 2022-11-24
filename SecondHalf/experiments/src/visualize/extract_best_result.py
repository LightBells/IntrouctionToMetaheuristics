import sys
sys.path.append('..')

import functions as f

import numpy as np
import pandas as pd

from tqdm import tqdm
import itertools


if __name__ == "__main__":
    # Read data from file
    de_data = pd.read_csv('../result/de_result_wo_quatic.csv', sep=',')
    ga_data = pd.read_csv('../result/ga_result.csv', sep=',')
    pso_data = pd.read_csv('../result/pso_result.csv', sep=',')

    data = pd.concat([de_data, ga_data, pso_data], ignore_index=True)


    # methods = ['genetic_algorithm', 'differential_evolution', 'partical_swarm_optimization']
    methods = ['genetic', 'differential_evolution', 'particle_swarm_optimization']
    
    # generate iteration list
    iteration = list(itertools.product(methods, f.meta_informations))

    df = pd.DataFrame(columns=['function', 'algorithm', 'population', 'value', 'time'])

    # Calculate the mean, max, min of each method for each population
    for method, function in tqdm(iteration):
        data_for_method = data[(data['algorithm'] == method) & (data['function'] == function['name'])][['algorithm', 'population', 'function','value', 'time']]

        candidate = data_for_method[data_for_method['value'] == data_for_method['value'].min()]
        if candidate.shape[0] > 1:
            candidate = candidate[candidate['time'] == candidate['time'].min()]
        # Extract the best result
        df = df.append(candidate, ignore_index=True)

    df.to_csv('../result/best_result.csv', index=False)

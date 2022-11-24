import sys
sys.path.append('..')

import functions as f

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import seaborn as sns

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

    # Calculate the mean, max, min of each method for each population
    for method, function in tqdm(iteration):
        data_for_method = data[(data['algorithm'] == method) & (data['function'] == function['name'])][['population', 'function','value', 'time']]


        # Plot the mean, max, min of each method for each population
        maxs = data_for_method.groupby('population').max()
        mins = data_for_method.groupby('population').min()
        plt.figure(figsize=(20, 5), dpi=200)

        g = sns.relplot(x='population', y='value', data=data_for_method, kind='line')
        g.map(sns.lineplot, x=maxs.index, y=maxs['value'], label='max', color = 'red')
        g.map(sns.lineplot, x=mins.index, y=mins['value'], label='min', color = 'green')
        plt.title('Objective Value of {} for {}'.format(method, function['name']))
        plt.grid()
        plt.savefig('../figures/objective_value_{}_{}.png'.format(function["name"], method))
        plt.close()

        # Plot the mean, max, min of each method for each time 
        plt.figure(figsize=(20, 5), dpi=200)

        g = sns.relplot(x='population', y='time', data=data_for_method, kind='line')
        g.map(sns.lineplot, x=maxs.index, y=maxs['time'], label='max', color = 'red')
        g.map(sns.lineplot, x=mins.index, y=mins['time'], label='min', color = 'green')
        plt.title('Time of {} for {}'.format(method, function['name'])) 
        plt.grid()
        plt.savefig('../figures/time_{}_{}.png'.format(function["name"], method))   

        plt.close()

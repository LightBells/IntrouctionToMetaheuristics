# タブーサーチ
from itertools import combinations
import os,sys,copy
import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

import urllib.request
url = 'https://raw.githubusercontent.com/maskot1977/ipython_notebook/master/toydata/location.txt'
urllib.request.urlretrieve(url, 'location.txt') # データのダウンロード

import pandas as pd
japan = pd.read_csv('location.txt')


import numpy as np
from scipy.spatial import distance

customerNum = 46
mat = japan[['Latitude', 'Longitude']].values
dist_mat = distance.cdist(mat, mat, metric='euclidean') # ユークリッド距離

distance_matrix = {}
for i, town in enumerate(japan['Town']):
    if town not in distance_matrix.keys():
        distance_matrix[town] = {}
    for j, town2 in enumerate(japan['Town']):
        distance_matrix[town][town2] = dist_mat[i][j]
    # print(distance_matrix)


class Tabu():
    def __init__(self,disMatrix,max_iters=50,maxTabuSize=10):
        """parameters definition"""
        self.disMatrix = disMatrix
        self.maxTabuSize = maxTabuSize
        self.max_iters = max_iters
        self.tabu_list=[]

    def get_route_distance(self,route):
        '''
        Description: function to calculate total distance of a route. evaluate function.
        parameters: route : list
        return : total distance : folat
        '''        
        routes = [0] + route + [0]    # add the start and end point 
        total_distance = 0
        for i,n in enumerate(routes):
            if i != 0 :
                total_distance = total_distance +  self.disMatrix[last_pos][n] 
            last_pos = n
        return total_distance

    def exchange(self,s1,s2,arr):
        """
        function to Swap positions of two elements in an arr
        Args: int,int,list
            s1 : target 1 
            s2 : target 2  
            arr : target array 
        Ouput: list
            current_list : target array 
        """
        current_list = copy.deepcopy(arr)
        index1 , index2 = current_list.index(s1) , current_list.index(s2)  # get index
        current_list[index1], current_list[index2]= arr[index2] , arr[index1]
        return current_list

    def generate_initial_solution(self,num=10,mode='greedy'):
        """
        function to get the initial solution,there two different way to generate route_init.
        Args: 
            num :  int
                the number of points 
            mode : string
                "greedy" : advance step by choosing optimal one 
                "random" : randomly generate a series number
        Ouput: list
            s_init : initial solution route_init
        """
        if mode == 'greedy':
            route_init=[0]
            for i in range(num):
                best_distance = 10000000
                for j in range(num+1):
                    if self.disMatrix[i][j] < best_distance and j not in route_init:  
                        best_distance = self.disMatrix[i][j]
                        best_candidate = j
                route_init.append(best_candidate)
                # route_init.append( list( distance_matrix.keys())[best_candidate] ) 
                
            route_init.remove(0)
                            
        if mode == 'random':
            route_init = np.arange(1,num+1)  #init solution from 1 to num
            np.random.shuffle(route_init)  #shuffle the list randomly

        return list(route_init)

    def tabu_search(self,s_init):   
        """tabu search"""
        s_best = s_init 
        bestCandidate = copy.deepcopy(s_best)
        routes , temp_tabu = [] , []   # init
        routes.append(s_best)
        while(self.max_iters):
            self.max_iters -= 1 # Number of iterations
            neighbors = copy.deepcopy(s_best)
            for s in combinations(neighbors, 2):   
                sCandidate = self.exchange(s[0],s[1],neighbors)  # exchange number to generate candidates
                if s not in self.tabu_list and self.get_route_distance(sCandidate) < self.get_route_distance(bestCandidate):
                    bestCandidate = sCandidate
                    temp_tabu = s                           
            if self.get_route_distance(bestCandidate) < self.get_route_distance(s_best): # record the best solution 
                s_best = bestCandidate
            if  temp_tabu not in self.tabu_list:
                self.tabu_list.append(temp_tabu)
            if len(self.tabu_list) > self.maxTabuSize :
                self.tabu_list.pop(0)
            routes.append(bestCandidate)
        return s_best, routes


import math,re,copy
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

class GetData():

    def generate_locations(self,num_points,map_size,num_vehicles=1,depot=0):
        """generate number of locations randomly in a block unit
            default TSP : num_vehicles=1,depot=0
        """
        locations=[]  # locations = [(24, 3), (21, 4), (5, 1),...] 
        for i in range(num_points):
            locations.append(tuple(np.random.randint(low=0,high=map_size,size=2))) 
        class random_data():
            def __init__(self):
                self.locations = locations
                self.num_vehicles = num_vehicles
                self.depot = depot
        return random_data()

    def get_euclidean_distance_matrix(self,locations):
        """Creates callback to return distance between locations."""
        distances = {}
        for from_counter, from_node in enumerate(locations):
            distances[from_counter] = {}
            for to_counter, to_node in enumerate(locations):
                if from_counter == to_counter:
                    distances[from_counter][to_counter] = 0
                else:
                    # Euclidean distance
                    distances[from_counter][to_counter] = (int(                        
                    math.hypot((from_node[0] - to_node[0]),
                                (from_node[1] - to_node[1]))))
        return distances


    def read_solomon(self,path,customerNum=100):
        '''Description: load solomon dataset'''        
        f = open(path, 'r')
        lines = f.readlines()
        locations,demand,readyTime,dueTime,serviceTime=[],[],[],[],[]
        for count,line in enumerate(lines):
            count = count + 1
            if(count == 5):  
                line = line[:-1].strip() 
                str = re.split(r" +", line)
                vehicleNum = int(str[0])
                capacity = float(str[1])
            elif(count >= 10 and count <= 10 + customerNum):
                line = line[:-1]
                str = re.split(r" +", line)
                locations.append((float(str[2]),float(str[3])))
                demand.append(float(str[4]))
                readyTime.append(float(str[5]))
                dueTime.append(float(str[6]))
                serviceTime.append(float(str[7]))
        class Solomon_data():
            def __init__(self):
                self.locations=locations
                self.demand = demand
                self.readyTime = readyTime
                self.dueTime = dueTime
                self.serviceTime = serviceTime
                self.vehicleNum = vehicleNum
                self.capacity =capacity
        return Solomon_data()

    
    def plot_nodes(self,locations):
        ''' function to plot locations'''
        Graph = nx.DiGraph()
        nodes_name = [str(x) for x in list(range(len(locations)))]
        Graph.add_nodes_from(nodes_name)
        pos_location = {nodes_name[i]:x for i,x in enumerate(locations)}
        nodes_color_dict = ['r'] + ['gray'] * (len(locations)-1)
        nx.draw_networkx(Graph,pos_location,node_size=200,node_color=nodes_color_dict,labels=None)  
        plt.show(Graph)

    def plot_route(self,locations,route,color='k'):
        ''' function to plot locations and route'''
        Graph = nx.DiGraph()
        edge = []
        edges = []
        for i in route : 
            edge.append(i)
            if len(edge) == 2 :
                edges.append(tuple(edge))
                edge.pop(0)
        nodes_name = [x for x in list(range(len(locations)))]
        Graph.add_nodes_from(nodes_name)
        Graph.add_edges_from(edges)
        pos_location = {nodes_name[i] : x for i,x in enumerate(locations)}
        nodes_color_dict = ['r'] + ['gray'] * (len(locations)-1)
        nx.draw_networkx(Graph,pos_location,node_size=200,node_color=nodes_color_dict,edge_color=color, labels=None)  
        plt.show(Graph)




if __name__ == "__main__":

    tsp = Tabu(disMatrix=dist_mat ,max_iters=20,maxTabuSize=10) 

	# two different way to generate initial solution
	# num : the number of points   
    s_init = tsp.generate_initial_solution(num=customerNum,mode='greedy') # mode = "greedy"  or "random"
    print('init route : ' , s_init)
    print('init distance : ' , tsp.get_route_distance(s_init))

    start = time.time()
    best_route , routes = tsp.tabu_search(s_init)     # tabu search
    end = time.time()

    print('best route : ' , best_route)
    print('best best_distance : ' , tsp.get_route_distance(best_route))
    print('the time cost : ',end - start )

    # plot the result changes with iterations
    results=[]
    for i in routes:
        results.append(tsp.get_route_distance(i))    
    # plt.plot(np.arange(len(results)) , results)
    # plt.show()
    
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(10, 10))
    Xs = []
    Ys = []
    for i in range(len(best_route)):
        # Xs.append(list(japan[japan['Town'] == best_route[i]].iloc[:, 2])[0])
        # Xs.append( list( distance_matrix.keys())[i] ) 
        # Xs.append(list(japan[i].iloc[:, 2])[0])
        Xs.append(list(japan[japan['Town'] == list( distance_matrix.keys())[i]].iloc[:, 2])[0])
        # Ys.append(list(japan[japan['Town'] == best_route[i]].iloc[:, 1])[0])
        # Ys.append(list(japan[i].iloc[:, 1])[0])
        Ys.append(list(japan[japan['Town'] == list( distance_matrix.keys())[i]].iloc[:, 1])[0])

    plt.plot(Xs, Ys)
    for city, x, y in zip(japan['Town'], japan['Latitude'], japan['Longitude']):
        plt.text(x, y, city, alpha=0.5, size=12)
    plt.grid()
    plt.show()
    fig.savefig("tsp_tabusearch.png")
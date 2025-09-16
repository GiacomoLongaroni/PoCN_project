import random 
import numpy as np
import igraph as ig 
from igraph import Graph

def generate_er_graph(n, z):
 
    p = z / (n - 1)
    g = Graph.Erdos_Renyi(n=n, p=p, directed=False, loops=False)
    edges = g.get_edgelist()
    return g, edges

def generate_ws_graph(n, z_target, beta=0.25):

    nei = max(1, int(round(z_target / 2.0)))    
    k_eff = 2 * nei
    g = ig.Graph.Watts_Strogatz(dim=1, size=n, nei=nei, p=beta, loops=False, multiple=False)
    edges = set(map(tuple, g.get_edgelist()))
    return g, edges, k_eff
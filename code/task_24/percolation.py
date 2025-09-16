import random
import numpy as np
import igraph as ig 
from scpp import *



def greedy_q_targets_by_degree(g, q_targets):
    
    n = g.vcount()
    degs = g.degree()

    star_center = []
    star_rays = set()
    
    for v in range(n):
        if v in star_rays:
            continue
        if degs[v] in q_targets:
            star_center.append(v)
            star_rays.update(g.neighbors(v))

    return star_center

def apply_qswap(g, q_targets):

    g2 = g.copy()
    star_centers = greedy_q_targets_by_degree(g2, q_targets)

    removed_edges = []
    added_edges = []

    for v in star_centers:
        neighbors = g2.neighbors(v)
        neighbors = np.sort(neighbors)
        q = len(neighbors)

        if q < 2:
            continue

        for u in neighbors:

            removed_edges.append(tuple(sorted((v, u))))

       
        for i in range(q):
            a = neighbors[i]
            b = neighbors[(i + 1) % q]
            added_edges.append(tuple(sorted((a, b))))

    if removed_edges:
        g2.delete_edges(removed_edges)
    if added_edges:
        g2.add_edges(added_edges)

    
    return g2, set(added_edges)


def quantum_percolation(g, swap_edges, p, use_distill):
    g2 = g.copy()

    
    p2 = scp(p, use_distill=use_distill)
    swap_set = {tuple(sorted(e)) for e in swap_edges}

    
    to_delete_ids = []
    edgelist = g2.get_edgelist()  

    for eid, (u, v) in enumerate(edgelist):
        e_norm = (u, v) if u <= v else (v, u)
        prob_keep = p if e_norm in swap_set else p2
       
        if random.random() > prob_keep:
            to_delete_ids.append(eid)

    if to_delete_ids:
        g2.delete_edges(to_delete_ids)

    return g2

def giant_component_fraction(g):

    comp = g.connected_components(mode="weak")

    return comp.giant().vcount() / g.vcount()

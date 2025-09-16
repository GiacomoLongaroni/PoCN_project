import warnings
import igraph as ig
from nodes import create_node_files
from edges import create_edge_files
from plotting import plot_city_graph
import os, json


def create_files():
    warnings.filterwarnings("ignore", message=".*loadtxt: input contained no data.*")
    print('Writing edge files...\n')
    create_edge_files()
    print('Writing node files...\n')
    create_node_files()
    print('Done!')


create_files()

from mpl_toolkits.basemap import Basemap
import pandas as pd
import igraph as ig 
from igraph import Graph
import matplotlib.pyplot as plt
import numpy as np

def create_world_dataset(pop):
    dataset = pd.read_csv('europe.csv', 
                          sep=';',
                          usecols= [1,6,13,19])

    dataset = dataset[dataset['Country Code']=='IT']
    dataset = dataset[dataset['Population'] > pop]

    dataset[['lat', 'lon']] = dataset['Coordinates'].str.split(',', expand=True)
    dataset = dataset.sort_values('Name')
    dataset = dataset[['Name', 'lat', 'lon', 'Population']]
    dataset['id'] = np.arange(1,len(dataset)+1) 

    return dataset

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)

    a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
    c = 2 * np.atan2(np.sqrt(a), np.sqrt(1-a))
    return R * c  

def create_edges(dataset, g):
    ids = dataset["id"].tolist()
    lats = dataset["lat"].astype('float32').tolist()
    lons = dataset["lon"].astype('float32').tolist()
    pops = dataset["Population"].astype('float32').tolist()

    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            lat_i, lon_i, pop_i = lats[i], lons[i], pops[i]
            lat_j, lon_j, pop_j = lats[j], lons[j], pops[j]
            dist_ij = haversine(lat_i, lon_i, lat_j, lon_j)

            if dist_ij <= 60:
                g.add_edge(i, j, color = 'blue')

def create_graph(dataset):
    g = Graph()
    g.add_vertices(dataset["id"].tolist())
    g.vs["lat"] = dataset["lat"].tolist()
    g.vs["lon"] = dataset["lon"].tolist()
    g.vs["Name"] = dataset["Name"].tolist()
    create_edges(dataset, g)
    simulate_satellite_links(dataset, g)
    return g

def simulate_satellite_links(dataset, g):
    dataset = dataset[dataset['Population'] > 5e5]
    ids = dataset["id"].tolist()
    lats = dataset["lat"].astype('float32').tolist()
    lons = dataset["lon"].astype('float32').tolist()
    names = dataset["Name"].astype('str').tolist()
    for i in range(len(ids)):
        for j in range(i+1, len(ids)):
            lat_i, lon_i, = lats[i], lons[i]
            lat_j, lon_j = lats[j], lons[j]
            dist_ij = haversine(lat_i, lon_i, lat_j, lon_j)

            if dist_ij <= 10:
                print(names[i],names[j])
                g.add_edge(i, j, color = 'green')

def plot_graph(dataset, world_graph):
    # mappa Europa
    fig, ax = plt.subplots(figsize=(12, 12))
    m = Basemap(projection="merc",
                llcrnrlat=36, urcrnrlat=48,   
                llcrnrlon=6, urcrnrlon=19,  
                resolution="l", ax=ax)

    m.drawcoastlines()
    m.drawcountries()

    # proietto nodi in coordinate mappa
    x, y = m(dataset["lon"].values.astype('float'), dataset["lat"].values.astype('float'))

    # disegno archi
    for edge in world_graph.get_edgelist():
        i, j = edge
        color = world_graph.es[world_graph.get_eid(i, j)]["color"]
        plt.plot([x[i], x[j]], [y[i], y[j]], "k-", lw=0.3, color = color)
    
    plt.scatter(x, y, color = 'red', s = 2)
    


    plt.show()
import os, json
import igraph as ig


def plot_city_graph(
    city,
    year,
    edges_dir='final_edge_files',
    nodes_dir='final_node_files',
    directed=False,
    vertex_size=4,
    bbox=(600, 600),
    margin=40,
    edge_curved=False,
    encoding='latin-1',
    swap_lonlat=False,
    return_graph=False
):
    edges_path = os.path.join(edges_dir, f"{city}_edges.json")
    nodes_path = os.path.join(nodes_dir, f"{city}_nodes.json")

    with open(edges_path, encoding="utf-8") as f:
        edges_data = json.load(f)


    edge_list = [(e['id_from'] - 1, e['id_to'] - 1) for e in edges_data[year]]

    with open(nodes_path, encoding=encoding) as f:
        nodes_data = json.load(f)

    node_indices_1b = [int(k) for k in nodes_data.keys()]
    n_vertices = max(node_indices_1b)
    positions = [None] * n_vertices

    for k_str, station in nodes_data.items():
        k = int(k_str)
        lat = station['lat']
        lon = station['lon']
        xy = (lon, lat) if swap_lonlat else (lat, lon)
        positions[k - 1] = xy

    positions = [(0.0, 0.0) if p is None else p for p in positions]

    g = ig.Graph(edges=edge_list, directed=directed)
    if g.vcount() > len(positions):
        positions.extend([(0.0, 0.0)] * (g.vcount() - len(positions)))

    plot_obj = ig.plot(
        g,
        layout=positions,
        vertex_size=vertex_size,
        bbox=bbox,
        margin=margin,
        edge_curved=edge_curved
    )
    return plot_obj

import os, re, json
import numpy as np
from nodes import create_node_dictionaries

def create_edges_dict():

    cities_dict_with, cities_dict_without = create_node_dictionaries()
    cities = ['Barcelona','Beijin','Berlin','Chicago','HongKong','London','Madrid','Mexico']
    file_2_dictionary = {}
    for city in cities:
        folderdir = os.path.join('Data',city,'topologies')
        ext = ('number.txt')
        city_dictionary = {}

        for path, dirc, files in os.walk(folderdir):
            for name in files:
                if name.endswith(ext):

                    path_string = name
                    match = re.match(r'.*([1-2][0-9]{3})', path_string)

                    year = match.group(1)
                    edgedata = np.loadtxt(folderdir + '/' + path_string, dtype=int)

                    dict_list = []

                    for row in edgedata:

                        node_from, node_to = row[0], row[1]

                        station_from = cities_dict_with[city][node_from]
                        station_to   = cities_dict_with[city][node_to]

                        # Numero massimo di linee disponibili (conta le chiavi che iniziano con "line_")
                        num_lines_from = sum(1 for k in station_from if k.startswith("line_"))
                        num_lines_to   = sum(1 for k in station_to   if k.startswith("line_"))

                        lines_from = [station_from[f'line_{i}'] for i in range(1, num_lines_from + 1)]
                        lines_to   = [station_to[f'line_{i}']   for i in range(1, num_lines_to + 1)]

                        lines = []

                        for line_from in lines_from:
                            for line_to in lines_to:

                                if line_from==line_to and line_from is not None:
                                    lines.append(line_from)
                                if not lines:
                                    lines.append('No Lines Matching')
                                    lines = list(filter(lambda x: x != "No Lines Matching", lines))
                                

                        dict_list.append({'id_from' : int(node_from), 'id_to' : int(node_to), 'lines': lines})
                        city_dictionary[str(year)] = dict_list

        file_2_dictionary[city] =  city_dictionary    

    return file_2_dictionary    

def create_edge_files():

    dic = create_edges_dict()
    result_path = 'final_edge_files'
    os.makedirs(result_path, exist_ok=True)

    for key, value in dic.items():

        file_path = os.path.join(result_path, f"{key}_edges.json")

        with open(file_path, 'w', encoding='Latin-1') as fp:
            json.dump(value, fp, indent=2, ensure_ascii=False)
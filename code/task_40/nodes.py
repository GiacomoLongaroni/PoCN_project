import os, re, json, warnings
import numpy as np
import pandas as pd

def create_node_dictionaries():

    cities = ['Berlin','Chicago','HongKong','London','Madrid','Mexico']
    cities_dict_with = {}
    cities_dict_without = {}

    ### ONLY FOR:                                               ###
    ###'Berlin','Chicago','HongKong','London','Madrid','Mexico' ###
    for city in cities:

        folderdir = os.path.join('Data',city)
        linesdir = os.path.join(folderdir,'lines')
        files = sorted([f for f in os.listdir(linesdir)])

        df = pd.DataFrame()
        
        for file in files:
    
            stations = pd.read_csv( os.path.join(linesdir, file),
                                    sep=r"\s+",
                                    engine="python",
                                    header=None,
                                    usecols=[0],
                                    encoding='Latin-1')

            station_line = os.path.basename(file).split('.')[0]

            df_a = pd.DataFrame()

            df_a["label"] = stations[0]
            df_a["line"] = station_line

            df = pd.concat([df, df_a], ignore_index=True)

            tmp = (df[['label', 'line']]
                   .drop_duplicates()
                   .sort_values(['label', 'line']))

            agg = tmp.groupby('label')['line'].apply(list)
            wide = agg.apply(pd.Series).add_prefix('line_')

            wide.columns = [f'line_{i}' for i in range(1, wide.shape[1]+1)]

        lines_df = wide.reset_index()
        data_path = os.path.join(folderdir, 'stations_dataset.txt')

        df = pd.read_csv(data_path,
                 sep=r"\s+",
                 engine="python",  
                 header=None,       
                 names=["label", "lat", "lon", "year"],
                 usecols=[0,1,2,3],
                 encoding='Latin-1')
        
        # preserving dataset id 
        node_id = np.arange(start=1,stop=len(df)+1, step=1)
        df['ID'] = node_id

        merged = pd.merge(df, lines_df, on="label", how="left")
        merged = merged.sort_values('ID')

        station_dict_with_lines = {}
        station_dict_without_lines = {}

        cols_with = merged.columns
        records_with = merged[cols_with].to_dict(orient="records")
        cols_without = cols_with[[0,1,2,3,4]]
        records_without = merged[cols_without].to_dict(orient="records")

        for obj in records_with:
            station_dict_with_lines[obj['ID']] = obj
        for obj in records_without:
            station_dict_without_lines[obj['ID']] = obj

        cities_dict_with[str(city)] = station_dict_with_lines
        cities_dict_without[str(city)] = station_dict_without_lines

    ### ONLY FOR:
    ### 'Barcelona','Beijin' ###

    cities = ['Barcelona','Beijin']

    for city in cities:

        station_dict_with_lines = {}
        station_dict_without_lines = {}

        folderdir = os.path.join('Data',city)
        df = pd.read_csv(
                         os.path.join(folderdir,'stations_dataset.txt'),
                         sep=r"\s+",
                         engine="python",  
                         header=None,
                         encoding='Latin-1',   
                         usecols=[0,1,2,3],  
                         names=["label", "lat", "lon", "year"])
        
        node_id = np.arange(start=1,stop=len(df)+1, step=1)
        df['ID'] = node_id


        line_files = os.path.join(folderdir,'stations_dataset+.txt')
        stations = []

        if city == 'Barcelona':


            pattern = re.compile(r"^(.*?)\s+.*?(Line\d+)", re.IGNORECASE)

            with open(line_files, "r", encoding="Latin-1") as f:
                for line in f:

                    match = pattern.search(line)
                    if match:
                        station = match.group(1).strip()
                        line_name = match.group(2).strip()
                        stations.append((station, line_name))

            df_dirty = pd.DataFrame(stations, columns=["label", "line"])

            agg = df_dirty.groupby('label')['line'].apply(list)
            wide = agg.apply(pd.Series).add_prefix('line_')
            wide.columns = [f'line_{i}' for i in range(1, wide.shape[1]+1)]

            lines_df = wide.reset_index()
            merged = pd.merge(df, lines_df, on="label", how="left")
            merged = merged.sort_values('ID')

            cols_with = merged.columns
            records_with = merged[cols_with].to_dict(orient="records")

            cols_without = cols_with[[0,1,2,3,4]]
            records_without = merged[cols_without].to_dict(orient="records")

            for obj in records_with:
                station_dict_with_lines[obj['ID']] = obj

            for obj in records_without:
                station_dict_without_lines[obj['ID']] = obj

            cities_dict_with[str(city)] = station_dict_with_lines
            cities_dict_without[str(city)] = station_dict_without_lines

        if city == 'Beijin':

            df = pd.read_csv(
                            os.path.join(folderdir,'stations_dataset.txt'),
                            sep=r"\s+",
                            engine="python",  
                            header=None,
                            encoding='Latin-1',     
                            names=["label", "lat", "lon", "year", 'line_1', 'line_2', 'line_3'])
            

            node_id = np.arange(start=1,stop=len(df)+1, step=1)
            df['ID'] = node_id
            cols = ["label", "lat", "lon", "year", 'ID', 'line_1', 'line_2', 'line_3']
            df = df[cols]

            cols_with = df.columns
            records_with = df[cols_with].to_dict(orient="records")

            cols_without = cols_with[[0,1,2,3,4]]
            records_without = df[cols_without].to_dict(orient="records")

            for obj in records_with:
                station_dict_with_lines[obj['ID']] = obj

            for obj in records_without:
                station_dict_without_lines[obj['ID']] = obj

            cities_dict_with[str(city)] = station_dict_with_lines
            cities_dict_without[str(city)] = station_dict_without_lines


    return cities_dict_with, cities_dict_without

def create_node_files():

    city_with, city_without = create_node_dictionaries()
    result_path = 'final_node_files'
    os.makedirs(result_path, exist_ok=True)

    for key, value in city_without.items():

        file_path = os.path.join(result_path, f"{key}_nodes.json")

        with open(file_path, 'w', encoding='Latin-1') as fp:
            json.dump(value, fp, indent=2, ensure_ascii=False)
from dataclasses import dataclass
import pandas as pd
import numpy as np
import requests
import os
import json

JSON_FILE_NAME = 'pokemon_data.json'
EXCEL_FILE_NAME = 'pokemon_data.xlsx'


@dataclass
class JSONtoEXCELconfig:
    FILE_DIR = os.path.join(os.getcwd(), 'pokemon')
    JSON_FILE_PATH = os.path.join(FILE_DIR, JSON_FILE_NAME)
    EXCEL_FILE_PATH = os.path.join(FILE_DIR, EXCEL_FILE_NAME)


class JSONtoEXCEL:
    def __init__(self) -> None:
        self.url = "https://raw.githubusercontent.com/Biuni/PokemonGO-Pokedex/master/pokedex.json"
        self.config = JSONtoEXCELconfig()


    def download_data(self):
        try:
            PATH = self.config.JSON_FILE_PATH
            dir_path = os.path.dirname(PATH)
            os.makedirs(dir_path, exist_ok=True)

            # Loading the json data from url
            pokemon_data = json.loads(requests.get(self.url).text)
            
            # Saving the json file to nasa folder (which is in working directory)
            with open(PATH, 'w') as f:
                json.dump(pokemon_data, f)
        except Exception as e:
            raise Exception(e)


    @staticmethod
    def list_of_int(list_):  
        try:
            data = list()
            for item in list_:
                data.append(round(item))
            return data
        except TypeError:
            return np.nan


    def initiate_data_structuring(self) -> pd.DataFrame:
        try:
            # Reading the data
            if not os.path.isfile(os.path.dirname(self.config.JSON_FILE_PATH)):
                self.download_data()
            data = pd.read_json(self.config.JSON_FILE_PATH)
            df = pd.json_normalize(data=data['pokemon'])


            # PROCESS TO CONVERT COLUMNS  DATATYPE FROM STRING TO FLOAT
            # columns datatype to be converted to float
            str_to_float = ['height', 'weight', 'egg']
            
            for col in str_to_float:
                # Replacing words or alphabets in columns with empty string
                df[col] = df[col].str.replace(r'[a-zA-z]', '', regex=True)
                df[col] = df[col].replace(r'^\s*$', np.nan, regex=True) # Replacing empty string with np.nan
                df[col] = df[col].fillna(0) # Imputing NaN values with 0
                
            # Converting column dtype from string to float 
            dict_columns_type = {'height': float, 'weight': float, 'egg': float}
            df = df.astype(dict_columns_type)


            # PROCESS TO CONVERT COLUMNS DATATYPE FROM STRING TO INT
            # Columns datatype to be converted to int
            str_to_int = ['id', 'num', 'candy_count', 'avg_spawns']
            for col_name in str_to_int:
                df[col_name] = df[col_name].fillna(0).astype(np.int64)


            # column 'type' should have strings and not list of strings.
            # Unpacking list contents in a column
            df['type'] = [','.join(map(str, l)) for l in df['type']]


            # column 'multipliers' - list of int
            df['multipliers'] = df['multipliers'].apply(lambda value: self.list_of_int(value))

            # Converting column 'spawn_time' to timedelta format
            df['spawn_time'] = df['spawn_time'].replace('N/A', '00:00')
            df['spawn_time'] = '00:' + df['spawn_time']
            df['spawn_time'] = pd.to_timedelta(df['spawn_time'])

            PATH = self.config.EXCEL_FILE_PATH
            dir_path = os.path.dirname(PATH)
            os.makedirs(dir_path, exist_ok=True)
            df.to_excel(PATH, index=False)
        
        except Exception as e:
            raise Exception(e)


if __name__ == '__main__':

    obj = JSONtoEXCEL()
    obj.initiate_data_structuring()

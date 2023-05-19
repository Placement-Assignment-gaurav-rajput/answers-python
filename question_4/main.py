'''
Excepted Output Data Attributes

    name - Name of Earth Meteorite - string 
    id - ID of Earth Meteorite - int 
    nametype - string 
    recclass - string
    mass - Mass of Earth Meteorite - float 
    year - Year at which Earth Meteorite was hit - datetime format 
    reclat - float 
    recclong - float
    point coordinates - list of int
'''


import os
from dataclasses import dataclass
import requests
import pandas as pd
import numpy as np
import json


JSON_FILE_NAME = 'meteorite_data.json'
EXCEL_FILE_NAME = 'meteorite_data.csv'


@dataclass
class DataFromAPIconfig:
    FILE_DIR = os.path.join(os.getcwd(), 'nasa')
    JSON_FILE_PATH = os.path.join(FILE_DIR, JSON_FILE_NAME)
    CSV_FILE_PATH = os.path.join(FILE_DIR, EXCEL_FILE_NAME)


class DataFromAPI:
    def __init__(self) -> None:
        self.url = "https://data.nasa.gov/resource/y77d-th95.json"
        self.config = DataFromAPIconfig()


    @staticmethod
    def list_of_int(list_):  
        '''This funtion converts the list of floats in a column to the list of int
        :params - list_ : list of floating point numbers
        :returns: list of int or NaN (if TypeError occurs, i.e, wrong input Datatype)
        '''
        try:
            data = list()
            for item in list_:
                data.append(round(item))
            return data
        except TypeError:
            return np.nan
        

    def download_data(self):
        try:
            PATH = self.config.JSON_FILE_PATH
            dir_path = os.path.dirname(PATH)
            os.makedirs(dir_path, exist_ok=True)

            nasa_data = dict()
            # Loading the json data from url
            response = json.loads(requests.get(self.url).text)
            
            nasa_data['nasa'] = response

            # Saving the json file to nasa folder (which is in working directory)
            with open(PATH, 'w') as f:
                json.dump(nasa_data, f)
        except Exception as e:
            raise Exception(e)


    def start(self) -> pd.DataFrame:
        try:

            # Reading the data
            if not os.path.isfile(os.path.dirname(self.config.JSON_FILE_PATH)):
                self.download_data()

            response = pd.read_json(self.config.JSON_FILE_PATH)

            dataframe = pd.DataFrame(pd.json_normalize(response['nasa']))

            # Dropping columns that are not required in final DataFrame
            dataframe.drop(['fall', 'geolocation.type',':@computed_region_cbhk_fwbd', ':@computed_region_nnqa_25f4' ], axis=1, inplace=True)

            # Converting 'id' column data-type to int
            dataframe['id'] = dataframe['id'].astype(np.int64)

            # COLUMNS TO FLOAT
            str_to_float =['mass', 'reclat', 'reclong']
            for col in str_to_float:
                dataframe[col] = dataframe[col].fillna(0).astype(np.float64)

            # Renaming 'geolocation.coordinates' to point coordinates
            dataframe.rename(columns={'geolocation.coordinates': 'point coordinates'}, inplace=True)

            # Changing column 'year' in datetime format
            dataframe['year'] = pd.to_datetime(dataframe['year'],format='%Y-%m-%dT%H:%M:%S.%f', errors= 'coerce')

            # column 'point coordinates' - list of int
            dataframe['point coordinates'] = dataframe['point coordinates'].apply(lambda value: self.list_of_int(value))

            PATH = self.config.CSV_FILE_PATH
            dir_path = os.path.dirname(PATH)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(PATH, index=False)

            csv_file = pd.read_csv(self.config.CSV_FILE_PATH)

            return csv_file
        
        except Exception as e:
            raise Exception(e)
    

if __name__ == '__main__':
    obj = DataFromAPI()
    print(obj.start())


'''
Excepted Output Data Attributes

id - int 
url - string
name - string 
season- int 
number - int
type - string 
airdate - date format 
airtime - 12-hour time format
runtime - float
average rating - float
summary - string (without html tags)
medium image link - string
Original image link - string
'''

import os
import requests
import pandas as pd
import json


class TvMaze:
    def __init__(self) -> None:
        self.api_link = "http://api.tvmaze.com/singlesearch/shows?q=westworld&embed=episodes"

    def start_api_call(self):
        try:
            response = json.loads(requests.get(self.api_link).text)
            df = pd.json_normalize(response['_embedded']['episodes'])
            
            # Renaming the columns
            df.rename(columns={'rating.average': 'average rating', 'image.medium':'medium image link', 'image.original':'Original image link'}, inplace=True)

            # Dropping the columns not present in col_list below
            col_list = ['id', 'url', 'name', 'season', 'number', 'type', 'airdate', 'airtime', 'runtime', 
            'average rating', 'summary', 'medium image link', 'Original image link']

            for col in df.columns:
                if col not in col_list:
                    df.drop(col, axis=1, inplace=True)

            # Removig the html tags from 'summary' column
            df['summary'] = df['summary'].str.replace(r'<.*?>', '', regex=True)

            # Converting 'airdate' to datetime format
            df['airdate'] = pd.to_datetime(df['airdate'])

            # Converting 'airtime' to 12-hour time format
            df['airtime'] = pd.to_datetime(df['airtime']).dt.strftime('%I:%M %p')

            # Converting the 'runtime' to float
            df['runtime'] = df['runtime'].astype(float)

            df.to_csv('question_5_output.csv', index=False)

            return df


        except Exception as e:
            raise Exception(e)
        


if __name__ == "__main__":
    obj = TvMaze()
    df = obj.start_api_call()
    print(df.columns)
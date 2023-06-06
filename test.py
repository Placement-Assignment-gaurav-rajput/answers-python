import pandas as pd

from question_4.main import DataFromAPI

obj = DataFromAPI()

file_csv_path = obj.config.CSV_FILE_PATH

df = pd.read_csv(file_csv_path)

print(df.columns)

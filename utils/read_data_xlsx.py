import pandas as pd
import from_root


file_path = from_root.from_root("assets/data.xlsx")

dataframe = pd.read_excel(file_path)

number_of_devices = len(dataframe.index)

def read_data_row(startIndex, stopIndex):
    for i in range(startIndex, stopIndex):
        print(dataframe["Tên HC"].iloc[i] + " | " + dataframe["Địa chỉ MAC"].iloc[i])


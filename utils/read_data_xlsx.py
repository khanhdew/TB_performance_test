import pandas as pd
import from_root

file_path = from_root.from_root("assets/data.xlsx")

class ReadDataXlsx:
    dataframe = pd.read_excel(file_path)
    number_of_devices = len(dataframe.index)
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ReadDataXlsx, cls).__new__(cls)
        return cls.instance

    def read_data_row(self, startIndex, stopIndex):
        for i in range(startIndex, stopIndex):
            print(self.dataframe["Tên HC"].iloc[i] + " | " + self.dataframe["Địa chỉ MAC"].iloc[i])



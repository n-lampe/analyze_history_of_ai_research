import numpy as np
import pandas as pd
import csv


class Purifier:

    def __init__(self, filename, config):
        self.convert(filename)
        self.drop_columns(filename, config.relevant_columns)
        self.dataset_to_lowercase(filename)
        self.clear(filename)

    def convert(self, filename):
        df = pd.read_excel("./" + filename + ".xlsx")
        print(df)
        df.to_csv("./" + filename + ".csv", sep=";")

    def drop_columns(self, filename, column_titles):
        f = pd.read_csv("./" + filename + ".csv", sep=";", low_memory=False)
        # print(f)
        new_f = pd.DataFrame(f[column_titles])
        print(new_f)
        for column_title in column_titles:
            if column_title == "time":
                dates = new_f[column_title].tolist()
                new_dates = self.format_year(dates)
                new_f = new_f.drop(columns=["time"])
                new_f['time'] = pd.Series(new_dates)
            continue
        print(new_f)
        new_f['time'] = pd.to_numeric(new_f['time'], errors='coerce')
        new_f = new_f.dropna(subset=['time'])
        new_f['time'] = new_f['time'].astype('int')
        new_f = new_f.rename(columns={"time": "Year"})
        print(new_f)
        new_f.to_csv("./" + filename + "_purified.csv", index=False)

    def drop_rows_without_time(self, dataframe):
        dataframe = dataframe[isinstance(dataframe.time, int)]
        return dataframe

    def dataset_to_lowercase(self, filename):
        f = pd.read_csv("./" + filename + "_purified.csv", low_memory=False)
        for label, content in f.items():
            f[label] = f[label].astype('str')
            f[label] = f[label].str.lower()
        f.to_csv("./" + filename + "_purified_lower.csv", index=False)

    def format_year(self, dates):
        new_dates = []
        start = 0
        end = 0
        for date in dates:
            try:
                start = date.rindex("-") + 1
            except:
                start = 0
            try:
                end = date.index(",")
            except:
                end = 0
            if start == 0:
                new_dates.append("0")
            elif end == 0:
                new_dates.append(date[start:])
            else:
                new_dates.append(date[start:end])

        return new_dates

    def clear(self, filename):
        import os
        os.remove("./" + filename + ".csv")
        os.remove("./" + filename + "_purified.csv")

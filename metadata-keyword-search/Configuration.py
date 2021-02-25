import pandas as pd
import csv
import os

class Configuration:
    keywords = pd.DataFrame()

    relevant_columns = []

    def __init__(self, filename):
        self.read_config(filename)
        self.read_keywords()

    def read_config(self, name_dataset):
        config = pd.read_excel("./config.xlsx")
        config.to_csv("./config.csv", sep=",")
        config = pd.read_csv("./config.csv")
        self.relevant_columns = config[name_dataset+".xlsx"].tolist()
        print(self.relevant_columns)
        self.relevant_columns = [x for x in self.relevant_columns if str(x) != 'nan']
        print(self.relevant_columns)
        os.remove("./config.csv")

    def read_keywords(self):
        keywords = pd.read_excel("./keywords.xlsx")
        #keywords.to_csv("./keywords.csv", sep=",")
        #config = pd.read_csv("./keywords.csv")
        perception = keywords['perception'].tolist()
        internal_processing = keywords['internal processing'].tolist()
        action = keywords['action'].tolist()
        nouns = keywords['nouns'].tolist()
        adjectives = keywords['adjectives'].tolist()
        environment = keywords['environment'].tolist()
        types = keywords['types'].tolist()
        #os.remove("./keywords.csv")
        self.keywords['perception'] = perception
        self.keywords['internal_processing'] = internal_processing
        self.keywords['action'] = action
        self.keywords['nouns'] = nouns
        self.keywords['adjectives'] = adjectives
        self.keywords['environment'] = environment
        self.keywords['types'] = types

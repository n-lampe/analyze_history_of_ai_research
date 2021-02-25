import math
import pandas as pd
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import MaxNLocator


class Analyzer:
    config = ""

    def __init__(self, filename, config):
        self.config = config
        print(self.count_Papers(filename))
        # self.papers_per_year("ICML_1988-2019")
        # self.papers_per_year_all_conferences_generic()
        # self.heatmap(self.papers_per_year_per_word(filename, "machine"), self.papers_per_year(filename))
        # self.combine(self.papers_per_year(filename), self.papers_per_year_per_word(filename, "machine"))
        # self.papers_per_year_for_all_words("ICML_1988-2019")
        # self.papers_per_year_in_percent(filename)
        # self.papers_per_year_per_word(filename, "machine")
        # self.percentage_of_papers_per_year_per_word(filename, "machine")
        # self.percentage_of_papers_all_conferences_per_year_per_word("machine")
        # self.average_percentage_of_papers_all_conferences_per_year_per_word("machine")
        # self.compare_arXiv_cs_ai_and_cs_all_ai_related()
        # self.data_of_heatmap_for_all_conferences("perception")
        # self.papers_per_year_per_word(filename, "human")

    def count_Papers(self, filename):
        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        counted_f = f.count()
        # print(pd.Series(counted_f))
        biggest = 0
        for value in f.count():
            # print(value)
            if value > biggest:
                biggest = value
        return biggest

    def papers_per_year(self, filename):
        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        f = (f['Year'].value_counts()).sort_index()
        if filename == "AITopics_1903-2018":
            #f.at[2018] = f.at[2018] * 6
            f = f.drop(labels=[0])
        return f

    def compare_arXiv_cs_ai_and_cs_all_ai_related(self):
        df_ai = self.papers_per_year("arXiv_cs_ai_1993-2018")
        df_ai_related = self.papers_per_year("arXiv_cs_ai-cl-cv-ml-ne_1993-2018")
        df_ai_related.at[2018] = df_ai_related.at[2018] * 4.5

        s = pd.concat([df_ai, df_ai_related], axis=1)
        print(s)
        s.plot(kind="bar")
        plt.xlabel('Year')
        plt.ylabel('Amount of papers')
        plt.title("Comparison of papers published in arXiv Computer Science subcategories")
        plt.legend(('Explicit AI', 'AI related'))
        plt.show()

    # Plots the amount of papers published in all conferences over the years
    def papers_per_year_all_conferences_generic(self):

        df_arXiv = pd.read_csv("./" + "arXiv_cs_ai_1993-2018" + "_purified_lower.csv")
        df_arXiv = (df_arXiv['Year'].value_counts()).sort_index()
        df_arXiv = df_arXiv.drop(labels=[1993, 1994, 1995, 1996, 2018])
        print(df_arXiv)

        df_AAAI = pd.read_csv("./" + "AAAI_1997-2017" + "_purified_lower.csv")
        df_AAAI = (df_AAAI['Year'].value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0], index=[2001, 2003, 2009])
        df_AAAI = df_AAAI.append(placeholder)
        df_AAAI = df_AAAI.sort_index()

        df_IJCAI = pd.read_csv("./" + "IJCAI_1997-2017" + "_purified_lower.csv", low_memory=False)
        df_IJCAI = df_IJCAI['Year']
        df_IJCAI = (df_IJCAI.value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0],
                                index=["1998", "2000", "2002", "2004", "2006", "2008", "2010", "2012", "2014"])
        df_IJCAI = df_IJCAI.append(placeholder)
        df_IJCAI = df_IJCAI.drop(labels='protect kern +.1667em')
        df_IJCAI = df_IJCAI.sort_index()

        df_ECAI = pd.read_csv("./" + "ECAI_2000-2016" + "_purified_lower.csv")
        df_ECAI = (df_ECAI['Year'].value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                index=[1997, 1998, 1999, 2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017])
        df_ECAI = df_ECAI.append(placeholder)
        df_ECAI = df_ECAI.sort_index()

        data = np.array([df_arXiv.values,
                         df_AAAI.values,
                         df_IJCAI.values,
                         df_ECAI.values])

        return data, df_AAAI.index

    # Counts the occurrence of given word in given paper over the years
    def papers_per_year_per_word(self, filename, word):
        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        try:
            list = (f['Year'].value_counts()).sort_index()
        except:
            list = (f['time'].value_counts()).sort_index()
        print(list)
        list.values[:] = 0
        print(list)
        f = f.set_index("Year")

        result_f = pd.DataFrame()

        print(result_f)

        for col in f.columns:
            s = pd.Series(f[col], dtype=str)
            container = s.str.contains(word, regex=False)
            result_f[container.name] = container

        print(result_f)

        for index, data in result_f.iterrows():
            row_series = pd.Series(data)
            if row_series.any():
                temp = list.loc[row_series.name] + 1
                list.at[row_series.name] = temp

        list = list.rename(word)
        print(list)
        return list

    # Plots how much percent of papers contain given word
    def percentage_of_papers_per_year_per_word(self, filename, word):
        word_occurences = self.papers_per_year_per_word(filename, word)
        paper_amounts = self.papers_per_year(filename)
        print(word_occurences)
        print(paper_amounts)
        word_occurences = word_occurences.multiply(100)
        result = word_occurences.divide(paper_amounts)
        if filename == "AITopics_1903-2018":
            result = result.drop(labels=[0, 1903, 1911, 1931, 1943, 1945, 1948, 1949, 1950, 1951, 1954, 1955])
        print(result)

        return result

    def percentage_of_papers_all_conferences_per_year_per_word(self, word):
        papers_arXiv = pd.read_csv("./" + "arXiv_cs_ai_1993-2018" + "_purified_lower.csv")
        papers_arXiv = (papers_arXiv['Year'].value_counts()).sort_index()
        papers_arXiv = papers_arXiv.drop(labels=[1993, 1994, 1995, 1996, 2018])
        # print(papers_arXiv)
        word_occurrences_arXiv = self.papers_per_year_per_word("arXiv_cs_ai_1993-2018", word)
        word_occurrences_arXiv = word_occurrences_arXiv.drop(labels=[1993, 1994, 1995, 1996, 2018])
        # print(word_occurrences_arXiv)
        word_occurrences_arXiv = word_occurrences_arXiv.multiply(100)
        df_arXiv = word_occurrences_arXiv.divide(papers_arXiv)
        print(df_arXiv)

        papers_AAAI = pd.read_csv("./" + "AAAI_1997-2017" + "_purified_lower.csv")
        papers_AAAI = (papers_AAAI['Year'].value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0], index=[2001, 2003, 2009])
        papers_AAAI = papers_AAAI.append(placeholder)
        papers_AAAI = papers_AAAI.sort_index()
        word_occurrences_AAAI = self.papers_per_year_per_word("AAAI_1997-2017", word)
        word_occurrences_AAAI = word_occurrences_AAAI.append(placeholder)
        word_occurrences_AAAI = word_occurrences_AAAI.sort_index()
        # print(word_occurrences_AAAI)
        word_occurrences_AAAI = word_occurrences_AAAI.multiply(100)
        df_AAAI = word_occurrences_AAAI.divide(papers_AAAI)
        print(df_AAAI)

        papers_IJCAI = pd.read_csv("./" + "IJCAI_1997-2017" + "_purified_lower.csv", low_memory=False)
        papers_IJCAI = papers_IJCAI['Year']
        papers_IJCAI = (papers_IJCAI.value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0],
                                index=["1998", "2000", "2002", "2004", "2006", "2008", "2010", "2012", "2014"])
        papers_IJCAI = papers_IJCAI.append(placeholder)
        papers_IJCAI = papers_IJCAI.drop(labels='protect kern +.1667em')
        papers_IJCAI = papers_IJCAI.sort_index()
        word_occurrences_IJCAI = self.papers_per_year_per_word("IJCAI_1997-2017", word)
        word_occurrences_IJCAI = word_occurrences_IJCAI.append(placeholder)
        word_occurrences_IJCAI = word_occurrences_IJCAI.sort_index()
        # print(word_occurrences_IJCAI)
        word_occurrences_IJCAI = word_occurrences_IJCAI.multiply(100)
        df_IJCAI = word_occurrences_IJCAI.divide(papers_IJCAI)
        df_IJCAI = df_IJCAI.drop(labels='protect kern +.1667em')
        print(df_IJCAI)
        df_IJCAI.index = df_IJCAI.index.astype(int)

        papers_ECAI = pd.read_csv("./" + "ECAI_2000-2016" + "_purified_lower.csv")
        papers_ECAI = (papers_ECAI['Year'].value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                index=[1997, 1998, 1999, 2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017])
        papers_ECAI = papers_ECAI.append(placeholder)
        papers_ECAI = papers_ECAI.sort_index()
        word_occurrences_ECAI = self.papers_per_year_per_word("ECAI_2000-2016", word)
        word_occurrences_ECAI = word_occurrences_ECAI.append(placeholder)
        word_occurrences_ECAI = word_occurrences_ECAI.sort_index()
        # print(word_occurrences_IJCAI)
        word_occurrences_ECAI = word_occurrences_ECAI.multiply(100)
        df_ECAI = word_occurrences_ECAI.divide(papers_ECAI)

        s = pd.concat([df_arXiv, df_AAAI, df_IJCAI, df_ECAI], axis=1)
        print(s)
        s.plot(kind="bar")
        plt.xlabel('Year')
        plt.ylabel('Papers in %')
        plt.title("Papers containing the word '" + word + "'")
        plt.legend(('arXiv>cs>ai', 'AAAI', 'IJCAI', 'ECAI'))
        plt.show()

    def average_percentage_of_papers_all_conferences_per_year_per_word(self, word):
        papers_arXiv = pd.read_csv("./" + "arXiv_cs_ai_1993-2018" + "_purified_lower.csv")
        papers_arXiv = (papers_arXiv['Year'].value_counts()).sort_index()
        papers_arXiv = papers_arXiv.drop(labels=[1993, 1994, 1995, 1996, 2018])
        # print(papers_arXiv)
        word_occurrences_arXiv = self.papers_per_year_per_word("arXiv_cs_ai_1993-2018", word)
        word_occurrences_arXiv = word_occurrences_arXiv.drop(labels=[1993, 1994, 1995, 1996, 2018])
        # print(word_occurrences_arXiv)
        word_occurrences_arXiv = word_occurrences_arXiv.multiply(100)
        df_arXiv = word_occurrences_arXiv.divide(papers_arXiv)
        print(df_arXiv)

        papers_AAAI = pd.read_csv("./" + "AAAI_1997-2017" + "_purified_lower.csv")
        papers_AAAI = (papers_AAAI['Year'].value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0], index=[2001, 2003, 2009])
        papers_AAAI = papers_AAAI.append(placeholder)
        papers_AAAI = papers_AAAI.sort_index()
        word_occurrences_AAAI = self.papers_per_year_per_word("AAAI_1997-2017", word)
        word_occurrences_AAAI = word_occurrences_AAAI.append(placeholder)
        word_occurrences_AAAI = word_occurrences_AAAI.sort_index()
        # print(word_occurrences_AAAI)
        word_occurrences_AAAI = word_occurrences_AAAI.multiply(100)
        df_AAAI = word_occurrences_AAAI.divide(papers_AAAI)
        print(df_AAAI)

        papers_IJCAI = pd.read_csv("./" + "IJCAI_1997-2017" + "_purified_lower.csv", low_memory=False)
        papers_IJCAI = papers_IJCAI['Year']
        papers_IJCAI = (papers_IJCAI.value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0],
                                index=["1998", "2000", "2002", "2004", "2006", "2008", "2010", "2012", "2014"])
        papers_IJCAI = papers_IJCAI.append(placeholder)
        papers_IJCAI = papers_IJCAI.drop(labels='protect kern +.1667em')
        papers_IJCAI = papers_IJCAI.sort_index()
        word_occurrences_IJCAI = self.papers_per_year_per_word("IJCAI_1997-2017", word)
        word_occurrences_IJCAI = word_occurrences_IJCAI.append(placeholder)
        word_occurrences_IJCAI = word_occurrences_IJCAI.sort_index()
        # print(word_occurrences_IJCAI)
        word_occurrences_IJCAI = word_occurrences_IJCAI.multiply(100)
        df_IJCAI = word_occurrences_IJCAI.divide(papers_IJCAI)
        df_IJCAI = df_IJCAI.drop(labels='protect kern +.1667em')
        print(df_IJCAI)
        df_IJCAI.index = df_IJCAI.index.astype(int)

        papers_ECAI = pd.read_csv("./" + "ECAI_2000-2016" + "_purified_lower.csv")
        papers_ECAI = (papers_ECAI['Year'].value_counts()).sort_index()
        placeholder = pd.Series([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                index=[1997, 1998, 1999, 2001, 2003, 2005, 2007, 2009, 2011, 2013, 2015, 2017])
        papers_ECAI = papers_ECAI.append(placeholder)
        papers_ECAI = papers_ECAI.sort_index()
        word_occurrences_ECAI = self.papers_per_year_per_word("ECAI_2000-2016", word)
        word_occurrences_ECAI = word_occurrences_ECAI.append(placeholder)
        word_occurrences_ECAI = word_occurrences_ECAI.sort_index()
        # print(word_occurrences_IJCAI)
        word_occurrences_ECAI = word_occurrences_ECAI.multiply(100)
        df_ECAI = word_occurrences_ECAI.divide(papers_ECAI)

        s = pd.concat([df_arXiv, df_AAAI, df_IJCAI, df_ECAI], axis=1)
        s['avg'] = s.mean(axis=1)
        print(s)
        return s['avg']

    def papers_per_year_for_all_words(self, filename):
        f = []
        for word in self.config.nouns:
            temp = self.papers_per_year_per_word(filename, word)
            # print(temp)
            f.append(temp)
            # print(f)
        s = pd.concat(f, axis=1)
        # print(s)
        sns.heatmap(s)
        plt.show()

    def combine(self, papers_per_year, papers_per_year_per_word):
        s = pd.concat([papers_per_year, papers_per_year_per_word], axis=1)
        # plt.plot(s)
        print(s)
        s.plot(kind="bar")
        plt.show()

    def data_of_heatmap_for_file(self, filename, word_category):
        df = pd.DataFrame
        array = []
        for keyword in self.config.keywords[word_category]:
            if not isinstance(keyword, str):
                break
            data = self.percentage_of_papers_per_year_per_word(filename, keyword)
            print(type(data))
            data.name = keyword
            array.append(data)

        df = pd.concat(array, axis=1)
        print(df)
        df = df.T
        print(df)
        return df

    def data_of_heatmap_custom_wordlist(self, filename, word_list):
        df = pd.DataFrame
        array = []
        for keyword in word_list:
            if not isinstance(keyword, str):
                break
            data = self.percentage_of_papers_per_year_per_word(filename, keyword)
            print(type(data))
            data.name = keyword
            array.append(data)

        df = pd.concat(array, axis=1)
        print(df)
        df = df.T
        print(df)
        return df

    def data_of_heatmap_for_all_conferences(self, word_category):
        df = pd.DataFrame()
        print(df)
        print(self.config.keywords)
        for keyword in self.config.keywords[word_category].tolist():
            if not isinstance(keyword, str):
                break
            data = self.average_percentage_of_papers_all_conferences_per_year_per_word(keyword)
            print(type(data))
            data.name = keyword
            df = df.append(data)
            print(df)

        print(df)
        return df

    def data_of_heatmap_for_all_conferences_custom_wordlist(self, word_list):
        df = pd.DataFrame()
        for keyword in word_list:
            if not isinstance(keyword, str):
                break
            data = self.average_percentage_of_papers_all_conferences_per_year_per_word(keyword)
            print(type(data))
            data.name = keyword
            df = df.append(data)
            print(df)

        print(df)
        return df

    def papers_per_year_in_percent(self, filename):
        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        print((f['Year'].value_counts()).sort_index())
        plt.plot((f['Year'].value_counts()).sort_index())
        new_f = (f['Year'].value_counts()).sort_index()
        papercounter = 0
        print(type(new_f))
        # print(new_f[0,4])
        for counter in range(1, new_f.size):
            print(new_f.loc[counter])
            papercounter = papercounter + new_f.loc[counter]
            new_f.loc[counter] = papercounter
            counter = counter + 1
        print(new_f)
        plt.show()
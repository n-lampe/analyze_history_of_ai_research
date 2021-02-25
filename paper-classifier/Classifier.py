import pandas as pd
from copy import deepcopy
from VocabularyReader import VocabularyReader


class Classifier:
    config = VocabularyReader()

    # Counts papers per year for given collection
    def count_papers_per_year(self, filename):
        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        try:
            list = (f['Year'].value_counts()).sort_index()
        except:
            list = (f['time'].value_counts()).sort_index()
        list = list.astype('float64')
        return list

    # Counts the occurrence of all words of given vocabulary for every paper in given collection
    def count_keywords_per_paper(self, filename, vocabulary):
        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        f = f.set_index("Year")
        result_f = pd.DataFrame()

        for word in vocabulary:
            i = 0
            for col in f.columns:
                s = pd.Series(f[col], dtype=str)
                container = s.str.count(word)
                if i == 0:
                    result_f[word] = container
                else:
                    temp = result_f[word].add(container)
                    result_f[word] = temp
                i = i + 1

        series = pd.Series([])

        for index, data in result_f.iterrows():
            row_series = pd.Series(data)
            sum = row_series.sum()
            series = series.append(pd.Series([sum], index=[index]))

        result_f["sum"] = series

        return result_f["sum"]

    # Counts keyword in given collection that are related to human intelligence or technical implementation of it
    # Calculates the difference between two
    # Depending on whether a paper has more to do with Hi or Ti, the sum of the Ti papers is subtracted from the sum of
    # the Hi papers
    # So there is a positive or negative total per year, depending on the preponderance of Hi / Ti papers in each year
    def get_hi_ti_comparison(self, filename):
        hi_series = self.count_keywords_per_paper(filename, self.config.hi_vocabulary)
        ti_series = self.count_keywords_per_paper(filename, self.config.ti_vocabulary)
        result_series = hi_series.sub(ti_series)

        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        try:
            list = (f['Year'].value_counts()).sort_index()
        except:
            list = (f['time'].value_counts()).sort_index()
        list.values[:] = 0

        for index, value in result_series.items():
            if value < 0:
                temp = list.loc[index] - 1
                list.at[index] = temp
            elif value > 0:
                temp = list.loc[index] + 1
                list.at[index] = temp

        list_float = list.astype('float64')
        return list_float

    # Puts Hi / Ti totals for multiple collections together in one big total
    # This total (per year) is divided by total of papers per year
    # The result is a comparison of Hi / Ti indicators in relation to papers per year
    def compare_hi_ti_indicators_for_multiple_collections_in_relation_to_papers_per_year(self):
        data = []
        hi_ti_arxiv = self.get_hi_ti_comparison("arXiv_cs_ai_1993-2018")
        amount_arxiv = self.count_papers_per_year("arXiv_cs_ai_1993-2018")

        hi_ti_aaai = self.get_hi_ti_comparison("AAAI_1997-2017")
        amount_aaai = self.count_papers_per_year("AAAI_1997-2017")

        hi_ti_ijcai = self.get_hi_ti_comparison("IJCAI_1997-2017")
        amount_ijcai = self.count_papers_per_year("IJCAI_1997-2017")

        hi_ti_ecai = self.get_hi_ti_comparison("ECAI_2000-2016")
        amount_ecai = self.count_papers_per_year("ECAI_2000-2016")

        temp1 = hi_ti_arxiv.add(hi_ti_aaai)
        temp2 = temp1.add(hi_ti_ijcai)
        hi_ti_sum = temp2.add(hi_ti_ecai)

        amount1 = amount_arxiv.add(amount_aaai)
        amount2 = amount1.add(amount_ijcai)
        amount_sum = amount2.add(amount_ecai)

        hi_ti_sum = hi_ti_sum.astype('float64')
        amount_sum = amount_sum.astype('float64')
        result = hi_ti_sum.div(amount_sum)
        return result

    # Receives comparison of HI / TI indicators for one collection
    # This total (per year) is divided by total of papers per year
    # The result is a comparison of Hi / Ti indicators in relation to papers per year
    def compare_hi_ti_indicators_in_relation_to_papers_per_year(self, filename):
        series = self.get_hi_ti_comparison(filename)

        f = pd.read_csv("./" + filename + "_purified_lower.csv")
        try:
            list = (f['Year'].value_counts()).sort_index()
        except:
            list = (f['time'].value_counts()).sort_index()
        save = pd.Series(deepcopy(list))
        list.values[:] = 0
        print(list)

        for index, value in series.items():
            if value < 0:
                temp = list.loc[index] - 1
                list.at[index] = temp
            elif value > 0:
                temp = list.loc[index] + 1
                list.at[index] = temp

        list_float = list.astype('float64')
        save_float = save.astype('float64')
        result = list_float.div(save_float)
        return result

    # Classifies every paper of given collection into AI subtopics and ML subtopics
    # At first keywords of AI and ML vocabularies are counted
    # Then the scores are calculated and the paper is classified
    # In the end this method summarizes classifications of papers by years
    def classify_papers_of_collection_into_AI_and_ML_subtopics(self, filename):
        ### Count keywords of each vocabulary in collection
        cv_series_proof = self.count_keywords_per_paper(filename, self.config.cv_proof)
        cv_series_proof = cv_series_proof.mul(3)
        cv_series_ind = self.count_keywords_per_paper(filename, self.config.cv_ind)
        cv_series = cv_series_proof.add(cv_series_ind)
        cv_series.name = "CV"

        si_series_proof = self.count_keywords_per_paper(filename, self.config.si_proof)
        si_series_proof = si_series_proof.mul(3)
        si_series_ind = self.count_keywords_per_paper(filename, self.config.si_ind)
        si_series = si_series_proof.add(si_series_ind)
        si_series.name = "KSI"

        nlp_series_proof = self.count_keywords_per_paper(filename, self.config.nlp_proof)
        nlp_series_proof = nlp_series_proof.mul(3)
        nlp_series_ind = self.count_keywords_per_paper(filename, self.config.nlp_ind)
        nlp_series = nlp_series_proof.add(nlp_series_ind)
        nlp_series.name = "NLP"

        es_series_proof = self.count_keywords_per_paper(filename, self.config.es_proof)
        es_series_proof = es_series_proof.mul(3)
        es_series_ind = self.count_keywords_per_paper(filename, self.config.es_ind)
        es_series = es_series_proof.add(es_series_ind)
        es_series.name = "ES"

        ml_series_proof = self.count_keywords_per_paper(filename, self.config.ml_proof)
        ml_series_proof = ml_series_proof.mul(3)
        ml_series_ind = self.count_keywords_per_paper(filename, self.config.ml_ind)
        ml_series = ml_series_proof.add(ml_series_ind)

        dl_series_proof = self.count_keywords_per_paper(filename, self.config.dl_proof)
        dl_series_proof = dl_series_proof.mul(3)
        dl_series_ind = self.count_keywords_per_paper(filename, self.config.dl_ind)
        dl_series = dl_series_proof.add(dl_series_ind)
        ml_series = ml_series.add(dl_series)

        nn_series_proof = self.count_keywords_per_paper(filename, self.config.nn_proof)
        nn_series_proof = nn_series_proof.mul(3)
        nn_series_ind = self.count_keywords_per_paper(filename, self.config.nn_ind)
        nn_series = nn_series_proof.add(nn_series_ind)
        ml_series = ml_series.add(nn_series)
        dl_series = dl_series.add(nn_series)
        dl_series.name = "DL/NN"

        sl_series_proof = self.count_keywords_per_paper(filename, self.config.sl_proof)
        sl_series_proof = sl_series_proof.mul(3)
        sl_series_ind = self.count_keywords_per_paper(filename, self.config.sl_ind)
        sl_series = sl_series_proof.add(sl_series_ind)
        ml_series = ml_series.add(sl_series)
        sl_series.name = "SL"

        ul_series_proof = self.count_keywords_per_paper(filename, self.config.ul_proof)
        ul_series_proof = ul_series_proof.mul(3)
        ul_series_ind = self.count_keywords_per_paper(filename, self.config.ul_ind)
        ul_series = ul_series_proof.add(ul_series_ind)
        ml_series = ml_series.add(ul_series)
        ul_series.name = "UL"

        rl_series_proof = self.count_keywords_per_paper(filename, self.config.rl_proof)
        rl_series_proof = rl_series_proof.mul(3)
        rl_series_ind = self.count_keywords_per_paper(filename, self.config.rl_ind)
        rl_series = rl_series_proof.add(rl_series_ind)
        ml_series = ml_series.add(rl_series)
        ml_series.name = "ML"
        rl_series.name = "RL"

        ### Rough classification into big subtopics of artificial intelligence
        result = pd.concat([cv_series, si_series, nlp_series, es_series, ml_series], axis=1).reset_index()
        year_col = result["Year"]
        result = result.drop(['Year'], axis=1)

        copy = deepcopy(result)
        for col in copy.columns:
            copy[col].values[:] = 0

        max_value_index = result.idxmax(axis=1)

        for index, value in max_value_index.items():
            temp = result.at[index, value]
            if temp > 0:
                copy.at[index, value] = 3
                result.at[index, value] = 0

        max_value_index = result.idxmax(axis=1)

        for index, value in max_value_index.items():
            temp = result.at[index, value]
            if temp > 0:
                copy.at[index, value] = 2
                result.at[index, value] = 0

        max_value_index = result.idxmax(axis=1)

        for index, value in max_value_index.items():
            temp = result.at[index, value]
            if temp > 0:
                copy.at[index, value] = 1
                result.at[index, value] = 0

        result.index = year_col
        copy.index = year_col

        final = pd.concat(
            [self.count_score_per_year(year_col, copy["CV"]), self.count_score_per_year(year_col, copy["KSI"]),
             self.count_score_per_year(year_col, copy["NLP"]), self.count_score_per_year(year_col, copy["ES"]),
             self.count_score_per_year(year_col, copy["ML"])], axis=1).reset_index()

        final.index = final['index']
        final = final.drop(['index'], axis=1)
        final = final.drop(index=['index'])

        final.to_csv("ai_einordnung_" + filename + ".csv")

        ### Fine classification into subtopics of machine learning
        result = pd.concat([dl_series, sl_series, ul_series, rl_series], axis=1).reset_index()
        year_col = result["Year"]
        result = result.drop(['Year'], axis=1)

        copy = deepcopy(result)
        for col in copy.columns:
            copy[col].values[:] = 0

        max_value_index = result.idxmax(axis=1)

        for index, value in max_value_index.items():
            temp = result.at[index, value]
            if temp > 0:
                copy.at[index, value] = 1
                result.at[index, value] = 0

        result.index = year_col
        copy.index = year_col

        final = pd.concat(
            [self.count_score_per_year(year_col, copy["DL/NN"]), self.count_score_per_year(year_col, copy["SL"]),
             self.count_score_per_year(year_col, copy["UL"]), self.count_score_per_year(year_col, copy["RL"])],
            axis=1).reset_index()

        final.index = final['index']
        final = final.drop(['index'], axis=1)
        final.to_csv("ml_einordnung_" + filename + ".csv")

    # Summarizes classifications of papers by years
    def count_score_per_year(self, year_col, data_col):
        print(data_col.index)
        data_col.index = year_col
        list = (year_col.value_counts()).sort_index()
        list.values[:] = 0

        for index, value in data_col.items():
            temp = list.loc[index]
            list.at[index] = temp + value

        list.name = data_col.name
        return list

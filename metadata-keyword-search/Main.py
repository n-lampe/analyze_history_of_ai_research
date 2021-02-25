import pandas as pd
import matplotlib.pyplot as plt
from Configuration import Configuration
from Purifier import Purifier
from Analyzer import Analyzer
from Visualizer import Visualizer

c = Configuration("AITopics_1903-2018")
#p = Purifier("AITopics_1903-2018", c)
a = Analyzer("ECAI_2000-2016", c)

v = Visualizer()

filenames = ["ICML_1988-2019"]
aitopics_keywords_ml = ["learn", "machine", "predict", "interact"]
aitopics_keywords_ps = ["problem", "solve", "knowledge", "system"]

ac_keywords_ml = ["learn", "machine", "predict", "social"]
ac_keywords_general = ["problem", "solve", "knowledge", "information", "ability", "improve"]

icml_keywords_1 = ["machine", "predict", "information"]
icml_keywords_2 = ["problem", "knowledge", "plan", "system"]

# Generate all heatmaps for all filenames
#for filename in filenames:
#    for category in c.keywords.columns:
#        heatmap_data = a.data_of_heatmap_for_file(filename, category)
#        v.visualize_heatmap(heatmap_data, category, filename)

# Generate all heatmaps for all filenames with custom word list
#for filename in filenames:
#    heatmap_data = a.data_of_heatmap_custom_wordlist(filename, icml_keywords_2)
#    v.visualize_heatmap(heatmap_data, "icml_keywords_2", filename)

# Generate all heatmaps for AllConferences
#for category in c.keywords.columns:
#    heatmap_data = a.data_of_heatmap_for_all_conferences(category)
#    v.visualize_heatmap(heatmap_data, category, "All-Conferences")

# Generate all heatmaps for AllConferences custom word list
#heatmap_data = a.data_of_heatmap_for_all_conferences_custom_wordlist(ac_keywords_general)
#v.visualize_heatmap(heatmap_data, "general", "All-Conferences")

# Generate diagrams with papers per year for all filenames
#for filename in filenames:
#    paper_per_year_data = a.papers_per_year(filename)
#    v.visualize_papers_per_year(filename, paper_per_year_data)

# Generate diagrams with papers per year for AllConferences
#(paper_per_year_data, indexes) = a.papers_per_year_all_conferences_generic()
#v.visualize_papers_per_year_all_conferences(paper_per_year_data, indexes)

# Generate diagrams with percentage of papers containing top words for all filenames
#for filename in filenames:
#    for (columnName, columnData) in c.keywords.iteritems():
#        for keyword in columnData.values:
#            if not isinstance(keyword, str):
#                break
#            data = a.percentage_of_papers_per_year_per_word(filename, keyword)
#            v.visualize_percentage_of_papers_per_year_per_word(filename, keyword, data)

# Generate diagrams with percentage of papers containing top words for AllConferences
#for (columnName, columnData) in c.keywords.iteritems():
#    for keyword in columnData.values:
#        if not isinstance(keyword, str):
#            break
#        data = a.average_percentage_of_papers_all_conferences_per_year_per_word(keyword)
#        v.visualize_average_percentage_of_papers_all_conferences_per_year_per_word(keyword, data)

# Generate Streamgraphs for all filenames
#for filename in filenames:
for category in c.keywords.columns:
    df = pd.DataFrame()
    array = []
    for keyword in c.keywords[category]:
        if not isinstance(keyword, str):
            break
        s = a.average_percentage_of_papers_all_conferences_per_year_per_word(keyword)
        s.name = keyword
        print(s)
        array.append(s)
        print(df)
    df = pd.concat(array, axis=1)
    df.plot()
    plt.xlabel('Year')
    plt.ylabel('% of papers')
    plt.title("Grouped_Dataset" + "_" + category)
    plt.legend(c.keywords[category])
    plt.savefig("streamgraphs\\all\\streamgraph_" + "combined_dataset" + "_" + category + ".png", bbox_inches='tight')
    plt.clf()



# Generate Streamgraphs for AllConferences

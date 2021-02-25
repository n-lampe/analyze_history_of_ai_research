import glob
import json
import os
import time
from datetime import timedelta

from pdfMiner import PdfMiner
from analyser import Analyser
from downloader import Downloader

test_path = "C:/dev/Intelligenzforschung/IJCAI_pdfs/"
test_file = "C:/dev/Intelligenzforschung/IJCAI_pdfs/1969_IJCAI/1969_IJCAI_1.pdf"

downloader = Downloader()
#downloader.download_from_single_volume_years([2005])
#downloader.download_from_double_volume_years([2001])

def create_word_count_json_for_IJCAI_documents(folder_path, out_file_folder_path):
    start_time = time.time()
    pdf_miner = PdfMiner()

    os.chdir(folder_path)
    sub_dir_list = glob.glob("*")
    dir_counter = 1
    for sub_dir in sub_dir_list:
        print("\rworking on " + sub_dir + "... (" + str(dir_counter) + "/" + str(len(sub_dir_list)) + ")")
        sub_dir_path = folder_path + "/" + sub_dir + "/"
        year = sub_dir.split("_")[0]
        year_data = pdf_miner.get_word_count_from_all_pdfs_in_folder(sub_dir_path)
        pdf_miner.save_year_data(out_file_folder_path, year, year_data)

        dir_counter += 1
        print("\rdone after " + str(timedelta(seconds=(time.time()-start_time))))

def create_word_count_json_for_one_year(folder_path, out_file_folder_path, year):
    start_time = time.time()
    pdf_miner = PdfMiner()
    year = str(year)
    year_data = pdf_miner.get_word_count_from_all_pdfs_in_folder(folder_path)
    pdf_miner.save_year_data(out_file_folder_path, year, year_data)

    print("\ndone after " + str(timedelta(seconds=(time.time()-start_time))))


# create_word_count_json_for_IJCAI_documents("C:/dev/Intelligenzforschung/IJCAI_pdfs/", "C:/dev/Intelligenzforschung/paper analyser/data/")
# create_word_count_json_for_one_year("C:/dev/Intelligenzforschung/IJCAI_pdfs/2001_IJCAI/", "C:/dev/Intelligenzforschung/paper analyser/data/", 2001)

# chart creation functions
analyser = Analyser("C:/dev/Intelligenzforschung/paper analyser/data/", ["1979", "2001"])

def create_charts_percentage_papers_containing_word(path):
    with open("words.json", 'r') as json_file:
        words = json.load(json_file)
    for word in words["perception"]:
        analyser.create_chart_percentage_of_papers_that_contain_the_word(word, path + "perception/")
    for word in words["internal_processing"]:
        analyser.create_chart_percentage_of_papers_that_contain_the_word(word, path + "internal_processing/")
    for word in words["action"]:
        analyser.create_chart_percentage_of_papers_that_contain_the_word(word, path + "action/")

def create_linegraph_charts_percentage_papers_containing_words(path):
    with open("words.json", 'r') as json_file:
        words = json.load(json_file)
    analyser.create_linegraph_percentage_of_papers_that_contain_the_words(words["perception"][:5], path, "papers_containing_" + "perception" + "_keywords.png")
    analyser.create_linegraph_percentage_of_papers_that_contain_the_words(words["action"][:5], path,
                                                                          "papers_containing_" + "action" + "_keywords.png")
    analyser.create_linegraph_percentage_of_papers_that_contain_the_words(words["internal_processing"][:5], path,
                                                                          "papers_containing_" + "internal_processing" + "_keywords.png")
    analyser.create_linegraph_percentage_of_papers_that_contain_the_words(words["keywords"], path,
                                                                          "papers_containing_keywords.png")

def create_word_frequency_heatmaps(path):
    with open("words.json", 'r') as json_file:
        words = json.load(json_file)
    analyser.create_chart_heatmap_of_word_frequency(words["perception"], path, "heatmap_word_frequency_perception")
    analyser.create_chart_heatmap_of_word_frequency(words["internal_processing"], path, "heatmap_word_frequency_internal_processing")
    analyser.create_chart_heatmap_of_word_frequency(words["action"], path, "heatmap_word_frequency_action")

# analyser.create_chart_total_papers_per_year("C:/dev/Intelligenzforschung/charts/")
# create_charts_percentage_papers_containing_word("C:/dev/Intelligenzforschung/charts/")
# create_linegraph_charts_percentage_papers_containing_words("C:/dev/Intelligenzforschung/charts/")
create_word_frequency_heatmaps("C:/dev/Intelligenzforschung/charts/")

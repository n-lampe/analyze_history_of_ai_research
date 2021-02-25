import json
import os
import glob
import re

from collections import Counter
from nltk.corpus import stopwords

import fitz


class PdfMiner:
    stop_words = list(stopwords.words('english'))
    stop_words.extend(['also'])

    def get_pdf_text(self, path):
        text = ""
        doc = fitz.open(path)
        for page in doc:
            text += page.getText(flags=0) + " "
        return text.lower()

    def filter_symbols(self, text):
        return re.sub(r'[.!?*+&%",;:\'`´’‘”“()\[\]{}]', ' ', text)

    def filter_stop_words(self, text):
        pattern = re.compile(r'\b(' + r'|'.join(self.stop_words) + r')\b\s*')
        return pattern.sub('', text)

    def get_word_count(self, text):
        return Counter([w for w in text.split() if len(w) > 1]).most_common()

    def get_word_count_from_pdf(self, path):
        text = self.get_pdf_text(path)
        text = self.filter_symbols(text)
        # text = self.filter_stop_words(text)
        return self.get_word_count(text)

    def get_word_count_from_all_pdfs_in_folder(self, path):
        year_data = []

        os.chdir(path)
        pdf_list = glob.glob("*.pdf")
        document_counter = 1
        for pdf in pdf_list:
            pdf_path = path + pdf
            print("\rworking on " + pdf_path + "... (" + str(document_counter) + "/" + str(len(pdf_list)) + ")",
                  end='')
            word_count = self.get_word_count_from_pdf(pdf_path)
            year_data.append({pdf: word_count})
            document_counter += 1
        return year_data

    def save_year_data(self, folder_path, year, data):
        outfile_path = folder_path + "/" + str(year) + ".json"
        with open(outfile_path, 'w') as json_file:
            json.dump(data, json_file)

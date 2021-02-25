from urllib.request import urlopen
import urllib.parse
import os
import time
from bs4 import BeautifulSoup


class Downloader:

    os.getcwd()

    # Single Volume: 1969 - 1975 & 2003 - ...
    def download_from_single_volume_years(self, years=list(range(1969, 1977, 2)) + list(range(2003, 2017, 2)) + list(range(2016, 2021))):
        start_time = time.time()

        for year in years:
            file_links = []
            base_url = "https://www.ijcai.org/Proceedings/" + str(year) + "/"
            response = urlopen(base_url)  # opens the URL
            page_source = response.read()
            soup = BeautifulSoup(page_source, 'html.parser')
            for link in soup.find_all('a'):
                current_link = link.get('href')
                if current_link.endswith('.pdf') and current_link not in file_links:
                    file_links.append(urllib.parse.urljoin(base_url, current_link))

            folder_name = str(year) + "_IJCAI"
            os.makedirs(folder_name)
            os.chdir(os.getcwd() + "/" + folder_name)

            file_counter = 0
            for file_link in file_links:
                try:
                    response = urlopen(file_link)
                    file = open(str(year) + "_IJCAI_" + str(file_counter) + ".pdf", 'wb')
                    file.write(response.read())
                    file.close()
                except:
                    print("error writing file: " + file_link)
                    pass
                finally:
                    file_counter = file_counter + 1
            os.chdir("..")

        print("--- %s seconds ---" % (time.time() - start_time))

    # Double Volume: 1977 - 2001
    def download_from_double_volume_years(self, years=list(range(1977, 2001, 2))):
        start_time = time.time()

        for year in years:
            file_links = []
            for j in [1, 2]:
                response = urlopen("https://www.ijcai.org/Proceedings/" + str(year) + "-" + str(j))  # opens the URL
                page_source = response.read()
                soup = BeautifulSoup(page_source, 'html.parser')
                for link in soup.find_all('a'):
                    current_link = link.get('href')
                    if current_link.endswith('.pdf') and current_link not in file_links:
                        file_links.append(current_link)

            folder_name = str(year) + "_IJCAI"
            os.makedirs(folder_name)
            os.chdir(os.getcwd() + "/" + folder_name)

            file_counter = 0
            for file_link in file_links:
                try:
                    response = urlopen(file_link)
                    file = open(str(year) + "_IJCAI_" + str(file_counter) + ".pdf", 'wb')
                    file.write(response.read())
                    file.close()
                except:
                    print("error writing file: " + file_link)
                    pass
                finally:
                    file_counter = file_counter + 1
            os.chdir("..")

        print("--- %s seconds ---" % (time.time() - start_time))

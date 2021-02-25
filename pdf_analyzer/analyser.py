import glob
import json
import os

import matplotlib.pyplot as plt
import matplotlib
import numpy as np


class Analyser:
    def __init__(self, data_folder_path, ignore_years=[]):
        self.data_folder_path = data_folder_path
        self.years_to_ignore = ignore_years

    def get_available_years(self):
        os.chdir(self.data_folder_path)
        json_files = glob.glob("*json")
        years = []
        for file in json_files:
            years.append(file.split(".")[0])
        return years

    def get_available_years_without_years_to_ignore(self):
        all_years = self.get_available_years()
        return [year for year in all_years if year not in self.years_to_ignore]

    def get_data_from_year(self, year):
        path = self.data_folder_path + str(year) + ".json"
        with open(path, 'r') as json_file:
            return json.load(json_file)

    def list_to_dict(self, list):
        return {list[i]: 0 for i in range(0, len(list))}


    def create_chart_total_papers_per_year(self, save_to_path=None):
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.92)

        plt.title('Total amount of papers per year')
        plt.xlabel('Year')
        plt.ylabel('Papers')

        x = []
        y = []

        for year in self.get_available_years():
            x.append(year)
            y.append(len(self.get_data_from_year(year)))
        plt.bar(x, y)
        if save_to_path is None:
            plt.show()
        else:
            plt.savefig(save_to_path + 'total_papers.png')
        plt.clf()

    def create_chart_percentage_of_papers_that_contain_the_word(self, search_word, save_to_path=None):
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.15, left=0.09, right=0.98, top=0.94)

        plt.title('Papers containing the word "' + search_word + '"')
        plt.xlabel('Years')
        plt.ylabel('Papers in %')

        x = []
        y = []

        for year in self.get_available_years_without_years_to_ignore():
            x.append(year)
            papers = self.get_data_from_year(year)
            total_papers = len(papers)
            papers_containing_the_word = 0
            for paper in papers:
                key = list(paper.keys())[0]
                word_count = paper[key]
                for word, frequency in word_count:
                    if search_word == word:
                        papers_containing_the_word += 1
                        break
            percentage = (papers_containing_the_word / total_papers) * 100
            y.append(percentage)

        plt.bar(x, y)
        if save_to_path is None:
            plt.show()
        else:
            plt.savefig(save_to_path + 'papers_containing_' + search_word + '.png')
        plt.clf()

    def create_linegraph_percentage_of_papers_that_contain_the_words(self, word_list, save_to_path=None, out_file_name="papers_containing_keywords.png"):
        plt.xticks(rotation=90)
        plt.subplots_adjust(bottom=0.15, left=0.09, right=0.75, top=0.94)

        plt.title('Papers containing specific keywords')
        plt.xlabel('Years')
        plt.ylabel('Papers in %')

        years = self.get_available_years_without_years_to_ignore()
        data = np.zeros((len(word_list), len(years)))

        for year_index, year in enumerate(years):
            papers = self.get_data_from_year(year)
            total_papers = len(papers)
            word_occurrences = self.list_to_dict(word_list)
            for paper in papers:
                key = list(paper.keys())[0]
                word_count = paper[key]
                for word, frequency in word_count:
                    for search_word in word_list:
                        if search_word == word:
                            word_occurrences[search_word] += 1
                            break
            for word_list_index, word in enumerate(word_list):
                percentage = (word_occurrences[word] / total_papers) * 100
                data[word_list_index][year_index] = percentage

        #plot it
        for word_index, word in enumerate(word_list):
            plt.plot(years, data[word_index], label=word)

        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)

        if save_to_path is None:
            plt.show()
        else:
            plt.savefig(save_to_path + out_file_name)
        plt.clf()

    def create_chart_heatmap_of_word_frequency(self, word_list, save_to_path=None, name="heatmap_word_frequency"):
        plt.subplots_adjust(bottom=0.2, left=0.05, right=1.2, top=0.99)

        years = self.get_available_years_without_years_to_ignore()

        data = np.zeros((len(word_list), len(years)))

        for year_index, year in enumerate(years):
            papers = self.get_data_from_year(year)
            total_words = 0
            word_occurrences = self.list_to_dict(word_list)
            for paper in papers:
                key = list(paper.keys())[0]
                word_count = paper[key]
                for word_in_paper, frequency in word_count:
                    for search_word in word_list:
                        if word_in_paper == search_word:
                            word_occurrences[search_word] += frequency
                    total_words += frequency
            for word_list_index, word in enumerate(word_list):
                percentage = (word_occurrences[word] / total_words) * 10000
                data[word_list_index][year_index] = percentage

        fig, ax = plt.subplots(figsize=(18, 8))

        im, cbar = heatmap(data, word_list, years, ax=ax,
                           cmap="YlGn", cbarlabel="word frequency in permyriad (per 10.000 words)")
        texts = annotate_heatmap(im, valfmt="{x:.3f}")

        fig.tight_layout()

        if save_to_path is None:
            plt.show()
        else:
            plt.savefig(save_to_path + name + '.png')
        plt.clf()


# helper heatmap functions from
# https://matplotlib.org/3.1.1/gallery/images_contours_and_fields/image_annotated_heatmap.html
def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw={}, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (N, M).
    row_labels
        A list or array of length N with the labels for the rows.
    col_labels
        A list or array of length M with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if not ax:
        ax = plt.gca()

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

    # We want to show all ticks...
    ax.set_xticks(np.arange(data.shape[1]))
    ax.set_yticks(np.arange(data.shape[0]))
    # ... and label them with the respective list entries.
    ax.set_xticklabels(col_labels)
    ax.set_yticklabels(row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    for edge, spine in ax.spines.items():
        spine.set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=["black", "white"],
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A list or array of two color specifications.  The first is used for
        values below a threshold, the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts
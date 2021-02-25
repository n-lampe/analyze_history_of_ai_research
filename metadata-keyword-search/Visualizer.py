import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


class Visualizer:

    def visualize_papers_per_year(self, filename, data):
        title = ""
        if filename == "AITopics_1903-2018":
            plt.subplots(figsize=(22, 12), dpi=300)
            title = "AITopics"
        else:
            plt.subplots(figsize=(15, 9), dpi=300)
            title = "ICML"
        data.plot(kind="bar", color="b")
        plt.xlabel('Year')
        plt.ylabel('Amount of papers')
        plt.title(title)
        mng = plt.get_current_fig_manager()
        mng.full_screen_toggle()
        plt.savefig("papers_per_year\\papers-per-year_" + filename + ".png", bbox_inches='tight')
        plt.clf()

    def visualize_papers_per_year_all_conferences(self, data, indexes):
        plt.subplots(figsize=(15, 9), dpi=300)
        color_list = ['b', 'r', 'g', 'm']

        x = indexes
        for i in range(data.shape[0]):
            plt.bar(x, data[i],
                    bottom=np.sum(data[:i], axis=0),
                    color=color_list[i % len(color_list)])

        plt.xlabel('Year')
        plt.ylabel('Amount of papers')
        plt.title("arXiv>cs>ai and the conferences AAAI, IJCAI and ECAI")
        plt.legend(('arXiv>cs>ai', 'AAAI', 'IJCAI', 'ECAI'))
        plt.savefig("papers_per_year\\papers-per-year_ALL_CONFERENCES.png", bbox_inches='tight')
        plt.clf()

    def visualize_percentage_of_papers_per_year_per_word(self, filename, word,  data):
        if filename == "AITopics_1903-2018":
            plt.subplots(figsize=(22, 12), dpi=300)
        else:
            plt.subplots(figsize=(15, 9), dpi=300)
        data.plot(kind="bar")
        plt.xlabel('Year')
        plt.ylabel('% of papers')
        if filename == "AITopics_1903-2018":
            plt.title("AITopics papers metadata containing the word '" + word + "'")
        else:
            plt.title("ICML papers metadata containing the word '" + word + "'")
        plt.savefig("word_percentages\\" + filename + "\\percentage_of_papers_with_" + word + "_.png", bbox_inches='tight')
        plt.clf()

    def visualize_average_percentage_of_papers_all_conferences_per_year_per_word(self, word, data):
        plt.subplots(figsize=(15, 9), dpi=300)
        data.plot(kind="bar")
        plt.xlabel('Year')
        plt.ylabel('% of papers')
        plt.title("Papers containing the word '" + word + "'")
        plt.legend(('Average (arXiv>cs>ai, AAAI, IJCAI, ECAI)',))
        plt.savefig("all_conferences_word_percentages\\percentage_of_papers_with_" + word + "_.png", bbox_inches='tight')
        plt.clf()

    def visualize_heatmap(self, data, word_category, identifier):
        if identifier == "AITopics_1903-2018":
            fig, ax = plt.subplots(figsize=(60, 20), dpi=300)
        elif identifier == "ICML_1988-2019":
            fig, ax = plt.subplots(figsize=(30, 18), dpi=300)
        else:
            fig, ax = plt.subplots(figsize=(22, 12), dpi=300)

        im, cbar = self.heatmap(data.values, data.index, data.columns, ax=ax,
                                cmap="YlGn", cbarlabel="Percentage of papers metadata containing the respective word")
        self.annotate_heatmap(im, valfmt="{x:.1f} %")

        plt.savefig("heatmaps\\heatmap_" + word_category + "_" + identifier + ".png", bbox_inches='tight')
        plt.clf()

    def heatmap(self, data, row_labels, col_labels, ax=None,
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

        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        return im, cbar

    def annotate_heatmap(self, im, data=None, valfmt="{x:.2f}",
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
            threshold = im.norm(data.max()) / 2.

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

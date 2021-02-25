from array import array
from copy import deepcopy

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.axes import Axes
from matplotlib.patches import Circle, RegularPolygon
from matplotlib.path import Path
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
from matplotlib.spines import Spine
from matplotlib.transforms import Affine2D


def radar_factory(num_vars, frame='polygon'):
    """
    Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle', 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    class RadarAxes(PolarAxes):

        name = 'radar'
        # use 1 line segment to connect specified points
        RESOLUTION = 1

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location('N')

        def fill(self, *args, closed=True, **kwargs):
            """Override fill so that line is closed by default"""
            return super().fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super().plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.append(x, x[0])
                y = np.append(y, y[0])
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            # The Axes patch must be centered at (0.5, 0.5) and of radius 0.5
            # in axes coordinates.
            if frame == 'circle':
                return Circle((0.5, 0.5), 0.5)
            elif frame == 'polygon':
                return RegularPolygon((0.5, 0.5), num_vars,
                                      radius=.5, edgecolor="k")
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

        def _gen_axes_spines(self):
            if frame == 'circle':
                return super()._gen_axes_spines()
            elif frame == 'polygon':
                # spine_type must be 'left'/'right'/'top'/'bottom'/'circle'.
                spine = Spine(axes=self,
                              spine_type='circle',
                              path=Path.unit_regular_polygon(num_vars))
                # unit_regular_polygon gives a polygon of radius 1 centered at
                # (0, 0) but we want a polygon of radius 0.5 centered at (0.5,
                # 0.5) in axes coordinates.
                spine.set_transform(Affine2D().scale(.5).translate(.5, .5)
                                    + self.transAxes)
                return {'polar': spine}
            else:
                raise ValueError("Unknown value for 'frame': %s" % frame)

    register_projection(RadarAxes)
    return theta


def visualize_AI_and_ML_classification(self, filename, collection_name, savename):
    # Visualize AI classification
    data = pd.read_csv("Einordnungen\\AI\\ai_einordnung_" + filename + ".csv")
    data = data.iloc[::-1]
    number_of_rows = len(data)

    counter = int(round(number_of_rows/5))
    relevant_rows = []
    for x in range(number_of_rows-1, 0, -counter):
        relevant_rows.append(x)

    copy = deepcopy(data)
    for index, data in data.iterrows():
        if index not in relevant_rows:
            copy = copy.drop(index)

    data = copy
    labels = data["index"]
    data = data.drop(['index'], axis=1)
    spoke_labels = data.columns
    data = data.to_numpy()

    N = len(spoke_labels)
    theta = radar_factory(N)

    fig, axes = plt.subplots(figsize=(9, 9), subplot_kw=dict(projection='radar'))

    cmap = matplotlib.cm.get_cmap('Blues')

    i = 0.3
    colors = []

    colors.append(cmap(i))
    y = 90/len(data)
    for i in range(10, 100, int(round(y))):
        temp = i / 100
        colors.append(cmap(temp))

    colors.reverse()

    axes.set_rgrids([])
    axes.set_title(collection_name, weight='bold', size='medium', position=(0.5, 1.1),
                   horizontalalignment='center', verticalalignment='center')
    for d, color in zip(data, colors):
        d = np.asarray(d)
        axes.plot(theta, d, color=color, linewidth=1.5)
        axes.fill(theta, d, facecolor=color, alpha=0.2)
    axes.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    legend = axes.legend(labels, loc=(0.9, .95),
                         labelspacing=0.1, fontsize='small')

    plt.savefig("Diagramme\\AI\\ai_classification" + savename + ".png", bbox_inches='tight')
    plt.clf()

    # Visualize ML classification
    data = pd.read_csv("Einordnungen\\ML\\ml_einordnung_" + filename + ".csv")
    data = data.iloc[::-1]
    number_of_rows = len(data)

    counter = int(round(number_of_rows/5))
    relevant_rows = []
    for x in range(number_of_rows-1, 0, -counter):
        relevant_rows.append(x)


    copy = deepcopy(data)
    for index, data in data.iterrows():
        if index not in relevant_rows:
            copy = copy.drop(index)

    data = copy
    labels = data["index"]
    data = data.drop(['index'], axis=1)
    spoke_labels = data.columns
    data = data.to_numpy()

    N = len(spoke_labels)
    theta = radar_factory(N)

    fig, axes = plt.subplots(figsize=(9, 9), subplot_kw=dict(projection='radar'))

    cmap = matplotlib.cm.get_cmap('Blues')
    rgba = cmap(0.5)

    i = 0.3
    colors = []

    colors.append(cmap(i))
    y = 90/len(data)
    for i in range(10, 100, int(round(y))):
        temp = i / 100
        colors.append(cmap(temp))

    colors.reverse()

    axes.set_rgrids([])
    axes.set_title(collection_name, weight='bold', size='medium', position=(0.5, 1.1),
                   horizontalalignment='center', verticalalignment='center')
    for d, color in zip(data, colors):
        d = np.asarray(d)
        axes.plot(theta, d, color=color, linewidth=1.5)
        axes.fill(theta, d, facecolor=color, alpha=0.2)
    axes.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    legend = axes.legend(labels, loc=(0.9, .95),
                         labelspacing=0.1, fontsize='small')

    plt.savefig("Diagramme\\AI\\ml_classification" + savename + ".png", bbox_inches='tight')
    plt.clf()


# -*- coding: utf-8 -*-
## @package palette.core.color_transfer
#
#  Color transfer.
#  @author      tody
#  @date        2015/09/16

import numpy as np
from scipy.interpolate import Rbf
from scipy.signal import resample
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from palette.plot.window import showMaximize
from palette.core.lab_slices import LabSlice, LabSlicePlot, Lab2rgb_py


## Color transfer for ab coordinates.
class ABTransfer:
    ## Constructor
    #  @param abs_original original ab coordinates.
    #  @param abs_edited   edited ab coordinates.
    def __init__(self, abs_original, abs_edited):
        abs_original = np.array(abs_original)
        abs_edited = np.array(abs_edited)
        rbf_a = Rbf(abs_original[:, 0], abs_original[:, 1], abs_edited[:, 0])
        rbf_b = Rbf(abs_original[:, 0], abs_original[:, 1], abs_edited[:, 1])
        self._rbf = [rbf_a, rbf_b]

    ## Color transfer for ab coordinates.
    def transfer(self, ab_original):
        abs_edited = [rbf(ab_original[0], ab_original[1]) for rbf in self._rbf]
        abs_edited = np.array(abs_edited)
        return abs_edited


## Simple plotter for ABTransfer.
class ABTransferPlot:
    ## Constructor
    #  @param abs_original     original ab coordinates.
    #  @param abs_edited       edited ab coordinates.
    #  @param L                target L coordinate.
    #  @param abs_animation    list of ab coordinates for plot animation.
    def __init__(self, abs_original, abs_edited, L=50, abs_animation=[]):
        self._slice = LabSlice(func=Lab2rgb_py)
        self._slice_plot = LabSlicePlot(self._slice)
        self._slice_plot.plot(L)
        self._abs_original = abs_original
        self._abs_edited = abs_edited
        self._abs_animation = abs_animation
        self._transfer = ABTransfer(abs_original, abs_edited)
        self._plot()

    ## Animation function for matplot.
    def animationFunc(self, step, *args):
        ab_id = step % len(self._abs_animation)

        ab_original = self._abs_animation[ab_id]
        xy_original, xy_edited = self._blendResult(ab_original)
        self._setArrow(self._blend_plot, xy_original, xy_edited)

        return self._blend_plot

    def _plot(self):
        xys_original = [self._slice.ab2xy(ab_original) for ab_original in self._abs_original]
        xys_edited = [self._slice.ab2xy(ab_edited) for ab_edited in self._abs_edited]
        for xy_original, xy_edited in zip(xys_original, xys_edited):
            self._arrow(xy_original, xy_edited)

        xy_original, xy_edited = self._blendResult(self._abs_animation[0])
        self._blend_plot = self._arrow(xy_original, xy_edited, color=[0.7, 0.5, 0.4])

    def _arrow(self, ps, pe, color=[1, 1, 1]):
        xs = [ps[0], pe[0]]
        ys = [ps[1], pe[1]]
        return [plt.plot(xs, ys, '-', color=color, linewidth=2, alpha=0.8)[0],
                plt.plot(ps[0], ps[1], 'o', color=color, linewidth=2, alpha=0.8)[0]]

    def _setArrow(self, arrow_plot, ps, pe):
        xs = [ps[0], pe[0]]
        ys = [ps[1], pe[1]]

        arrow_plot[0].set_data(xs, ys)
        arrow_plot[1].set_data(ps[0], ps[1])

    def _blendResult(self, ab_original):
        ab_edited = self._transfer.transfer(ab_original)
        xy_original = self._slice.ab2xy(ab_original)
        xy_edited = self._slice.ab2xy(ab_edited)
        return xy_original, xy_edited


## Simple color transfer demo.
def colorTransferAnimation():
    fig = plt.figure()
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

    font_size = 15
    fig.suptitle("Color Transfer (Animation)", fontsize=font_size)

    ab_original = [(-10, -20), (-20, 10), (40, 20)]
    ab_edited = [(30, -50), (10, 30), (60, -20)]

    abs_points = [(0, 0), (-20, 10), (0, -30), (-20, 10), (-20, 20), (40, 20), (40, -10)]
    abs_animation = resample(abs_points, num=100)

    transfer_plot = ABTransferPlot(ab_original, ab_edited, abs_animation=abs_animation)

    ani = animation.FuncAnimation(fig, transfer_plot.animationFunc, interval=10, blit=True)

    showMaximize()

if __name__ == '__main__':
    colorTransferAnimation()


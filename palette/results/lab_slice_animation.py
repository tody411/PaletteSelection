# -*- coding: utf-8 -*-
## @package palette.results.lab_slice_animation
#
#  Lab slice animation.
#  @author      tody
#  @date        2015/09/16

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from palette.core.lab_slices import LabSlicePlot, LabSlice, Lab2rgb_cv, Lab2rgb_py
from palette.plot.window import showMaximize


## Simple Lab slice plot animation.
def labSliceAnimation():
    fig = plt.figure()
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

    font_size = 15
    fig.suptitle("Lab slice (Animation)", fontsize=font_size)
    plt.subplot(1, 2, 1)
    plt.title("OpenCV Lab2rgb", fontsize=font_size)
    lab_plot_cv = LabSlicePlot(LabSlice(func=Lab2rgb_cv))

    plt.subplot(1, 2, 2)
    plt.title("Implemented Lab2rgb", fontsize=font_size)
    lab_plot_py = LabSlicePlot(LabSlice(func=Lab2rgb_py))

    def animFunc(step, *args):
        plots = lab_plot_cv.animationFunc(step)
        plots.extend(lab_plot_py.animationFunc(step))
        plt.draw()
        return plots

    ani = animation.FuncAnimation(fig, animFunc, interval=0, blit=True)

    showMaximize()

if __name__ == '__main__':
    labSliceAnimation()
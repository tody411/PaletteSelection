
# -*- coding: utf-8 -*-
## @package palette.results.color_transfer_demo
#
#  Simple color transfer demo.
#  @author      tody
#  @date        2015/09/16

from scipy.signal import resample
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from palette.plot.window import showMaximize
from palette.core.color_transfer import ABTransferPlot
from palette.plot.fig2np import figure2numpy
from palette.results.results import resultFile
from palette.io_util.video import saveVideo


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


## Simple color transfer demo.
def colorTransferVideo(figsize=(12, 6)):
    fig = plt.figure()
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

    font_size = 15
    fig.suptitle("Color Transfer (Animation)", fontsize=font_size)

    ab_original = [(-10, -20), (-20, 10), (40, 20)]
    ab_edited = [(30, -50), (10, 30), (60, -20)]

    abs_points = [(0, 0), (-20, 10), (0, -30), (-20, 10), (-20, 20), (40, 20), (40, -10)]
    abs_animation = resample(abs_points, num=100)

    transfer_plot = ABTransferPlot(ab_original, ab_edited, abs_animation=abs_animation)

    def animFunc(step, *args):
        transfer_plot.animationFunc(step)
        return figure2numpy(fig)

    images = [animFunc(step) for step in range(2*len(abs_animation))]
    result_file = resultFile("ColorTransfer", ".wmv")
    saveVideo(result_file, images)

if __name__ == '__main__':
    colorTransferVideo()


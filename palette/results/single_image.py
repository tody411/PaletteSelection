# -*- coding: utf-8 -*-
## @package palette.results.single_image
#
#  Demo for single image.
#  @author      tody
#  @date        2015/08/29


import os
import matplotlib.pyplot as plt

from palette.results.results import batchResults, resultFile
from palette.io_util.image import loadRGB
from palette.core.hist_3d import Hist3D
from palette.core.palette_selection import PaletteSelection
from palette.plot.window import showMaximize


## Demo for the single image file.
def singleImageResult(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    image = loadRGB(image_file)

    fig = plt.figure(figsize=(10, 7))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

    font_size = 15
    fig.suptitle("Palette Selection for Single Image", fontsize=font_size)

    fig.add_subplot(231)
    h, w = image.shape[:2]
    plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
    plt.imshow(image)
    plt.axis('off')

    color_spaces = ["rgb", "Lab"]
    sigmas = [0.7, 70.0]

    plot_id = 232
    num_cols = 3

    for color_space, sigma in zip(color_spaces, sigmas):
        hist3D = Hist3D(image, num_bins=16, color_space=color_space)
        color_coordinates = hist3D.colorCoordinates()
        color_densities = hist3D.colorDensities()
        rgb_colors = hist3D.rgbColors()

        palette_selection = PaletteSelection(color_coordinates,
                                             color_densities, rgb_colors,
                                             num_colors=5, sigma=sigma)

        plt.subplot(plot_id)
        plt.title("Palette Colors from %s" % color_space)
        palette_selection.plot(plt)
        plt.axis('off')

        plot_id += 1

        ax = fig.add_subplot(plot_id, projection='3d')
        plt.title("%s 3D Histogram" % color_space, fontsize=font_size)
        hist3D.plot(ax)

        plot_id += num_cols - 1

    result_file = resultFile("%s_single" % image_name)
    plt.savefig(result_file)
    #showMaximize()


## Demo for the given data names, ids.
def signleImageResults(data_names, data_ids):
    batchResults(data_names, data_ids, singleImageResult, "Palette Selection (single image)")

if __name__ == '__main__':
    data_names = ["apple", "flower", "tulip"]
    data_ids = [0, 1, 2]

    signleImageResults(data_names, data_ids)


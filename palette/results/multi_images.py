# -*- coding: utf-8 -*-
## @package palette.results.multi_images
#
#  Palette selection demo for multi images.
#  @author      tody
#  @date        2015/08/29

import os
import numpy as np
import matplotlib.pyplot as plt

from palette.results.results import batchDataGroup, resultFile
from palette.datasets.google_image import dataFile
from palette.io_util.image import loadRGB
from palette.core.color_pixels import ColorPixels
from palette.core.hist_3d import Hist3D
from palette.core.palette_selection import PaletteSelection
from palette.plot.window import showMaximize


## Compute palette selection result for the image file.
def paletteSelectionDataGroupMulti(data_name, data_ids):

    num_cols = len(data_ids)
    num_rows = 2

    fig = plt.figure(figsize=(10, 7))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.9, wspace=0.1, hspace=0.2)

    font_size = 15
    fig.suptitle("Palette Selection for Multi Images", fontsize=font_size)

    rgb_pixels = []
    plot_id = num_rows * 100 + 10 * num_cols + 1
    for data_id in data_ids:
        image_file = dataFile(data_name, data_id)
        image = loadRGB(image_file)

        rgb_pixels.extend(ColorPixels(image).rgb())

        fig.add_subplot(plot_id)
        h, w = image.shape[:2]
        plt.title("Original Image: %s x %s" % (w, h), fontsize=font_size)
        plt.imshow(image)
        plt.axis('off')

        plot_id += 1

    color_space = "Lab"
    sigma = 70.0

    plot_id = num_rows * 100 + 10 * num_cols + num_cols + 2

    rgb_pixels = np.array(rgb_pixels)
    print rgb_pixels.shape
    multi_image = np.array(rgb_pixels).reshape(1, -1, 3)

    hist3D = Hist3D(multi_image, num_bins=16, color_space=color_space)
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

    result_file = resultFile("%s_multi" % data_name)
    plt.savefig(result_file)


## Compute palette selection results for the given data names, ids.
def paletteSelectionResultsMulti(data_names, data_ids):
    batchDataGroup(data_names, data_ids, paletteSelectionDataGroupMulti, "Palette Selection (multi images)")

if __name__ == '__main__':
    data_names = ["apple", "flower", "tulip"]
    data_ids = [0, 1, 2]

    paletteSelectionResultsMulti(data_names, data_ids)
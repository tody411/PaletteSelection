# -*- coding: utf-8 -*-
## @package palette.core.palette_selection
#
#  Implementation of automatic color palette selection.
#  @author      tody
#  @date        2015/08/20

import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2

from palette.datasets.google_image import dataFile
from palette.cv.image import to32F, rgb2Lab, Lab2rgb
from palette.io_util.image import loadRGB
from palette.plot.window import showMaximize
from palette.results.results import resultFile
from palette.core.color_samples import Hist3D
from palette.np.norm import normVectors


## Implementation of automatic palette selection.
class PaletteSelection:
    ## Constructor
    #  @param color_samples     input color samples.
    #  @param color_densities   color densities (normalized frequencies).
    def __init__(self, color_samples, color_densities, num_colors=7, sigma=70.0, color_space="rgb"):
        self._color_samples = color_samples
        self._color_densities = color_densities
        self._num_colors = num_colors
        self._sigma = sigma
        self._color_space = color_space
        self._palette_colors = []

        self._computeDarkBrightColors()
        self._computeInitialWeight()

    def paletteColors(self):
        return self._palette_colors

    def rgbPaletteColors(self):
        palette_colors = np.array(self._palette_colors)
        rgb_colors = palette_colors
        if self._color_space == "Lab":
            rgb_colors = Lab2rgb(np.float32(palette_colors.reshape(1, -1, 3))).reshape(-1, 3)
        return rgb_colors

    def compute(self):
        for i in xrange(self._num_colors):
            palette_color = self._updatePalette()
            self._updateWeight(palette_color)

    def _computeDarkBrightColors(self):
        color_samples = self._color_samples

        intensities = normVectors(color_samples)
        c_dark = color_samples[np.argmin(intensities)]
        c_bright = color_samples[np.argmax(intensities)]
        self._dark_bright = [c_dark, c_bright]

    def _computeInitialWeight(self):
        self._color_weights = np.array(self._color_densities)
        self._updateWeight(self._dark_bright[0])
        self._updateWeight(self._dark_bright[1])

    def _updatePalette(self):
        color_id = np.argmax(self._color_weights)
        palette_color = self._color_samples[color_id]
        self._palette_colors.append(palette_color)
        return palette_color

    def _updateWeight(self, palette_color):
        dists = normVectors(self._color_samples - palette_color)
        factors = 1.0 - np.exp(- dists ** 2 / (self._sigma ** 2))
        self._color_weights = factors * self._color_weights

    def paletteImage(self, size=16, spacing=4):
        palette_colors = self.rgbPaletteColors()
        num_colors = len(self._palette_colors)

        w = num_colors * size + (num_colors - 1) * spacing
        h = size

        palette_image = np.zeros((h, w, 4), dtype=np.float)

        for i, palette_color in enumerate(palette_colors):
            x_min = i * size + i * spacing
            x_max = x_min + size

            palette_image[:, x_min:x_max, 0:3] = palette_color
            palette_image[:, x_min:x_max, 3] = 1.0
        return palette_image

    def plotPaletteColors(self, plt):
        palette_image = self.paletteImage()
        plt.imshow(palette_image)


def runPaletteSelectionResult(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    C_8U = loadRGB(image_file)
    C_32F = to32F(C_8U)
    Lab_32F = rgb2Lab(C_32F)

    fig = plt.figure(figsize=(10, 8))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.05)
    plt.title("Automatic Color Palette Selection")
    plt.subplot2grid((2, 2), (0, 0), rowspan=2)
    plt.title("%s" % (image_name))
    plt.imshow(C_32F)
    plt.axis('off')

    color_space = "rgb"

    hist3d = Hist3D(C_32F, num_bins=16, color_space=color_space)
    color_samples = hist3d.colorSamples()

    color_densities = hist3d.colorDensities()

    ax = fig.add_subplot(224, projection='3d')
    plt.title("3D Color Histogram")
    hist3d.plotColorSamples(ax)

    palette_selection = PaletteSelection(color_samples, color_densities, color_space=color_space)
    palette_selection.compute()

    plt.subplot(222)
    plt.title("Palette Colors")
    palette_selection.plotPaletteColors(plt)

    plt.axis('off')

    result_file = resultFile(image_name)
    plt.savefig(result_file)


def runPaletteSelectionResults(data_names, data_ids):
    for data_name in data_names:
        print "Palette Selection: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            runPaletteSelectionResult(image_file)


if __name__ == '__main__':
    data_names = ["apple", "tulip", "flower"]
    data_names = ["mip"]
    data_ids = [0, 1, 2, 3]

    runPaletteSelectionResults(data_names, data_ids)


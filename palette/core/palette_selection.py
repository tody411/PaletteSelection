# -*- coding: utf-8 -*-
## @package palette.core.palette_selection
#
#  Implementation of automatic color palette selection.
#  @author      tody
#  @date        2015/08/20

import os
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from palette.np.norm import normVectors


## Implementation of automatic palette selection.
class PaletteSelection:
    ## Constructor
    #  @param color_coordinates     input color coordinates.
    #  @param color_densities       color densities (normalized frequencies).
    #  @param rgb_colors            rgb colors.
    #  @param num_colors            target number of palette selection.
    #  @param sigma                 weight decay term for updating weight.
    def __init__(self, color_coordinates, color_densities, rgb_colors,
                 num_colors=7, sigma=70.0):
        self._color_coordinates = color_coordinates
        self._color_densities = color_densities
        self._rgb_colors = rgb_colors
        self._num_colors = num_colors
        self._sigma = sigma

        self._palette_coordinates = []
        self._palette_colors = []

        self._computeDarkBrightColors()
        self._computeInitialWeight()

        self._compute()

        self._plotter = PaletteSelectionPlot(self)

    def plot(self, plt):
        self._plotter.plot(plt)

    def paletteCoordinates(self):
        return self._palette_coordinates

    def paletteColors(self):
        return self._palette_colors

    def _compute(self):
        for i in xrange(self._num_colors):
            palette_coordinate = self._updatePalette()
            self._updateWeight(palette_coordinate)

    def _computeDarkBrightColors(self):
        rgb_colors = self._rgb_colors

        intensities = normVectors(rgb_colors)
        c_dark = self._color_coordinates[np.argmin(intensities)]
        c_bright = self._color_coordinates[np.argmax(intensities)]
        self._dark_bright = [c_dark, c_bright]

    def _computeInitialWeight(self):
        self._color_weights = np.array(self._color_densities)
        self._updateWeight(self._dark_bright[0])
        self._updateWeight(self._dark_bright[1])

    def _updatePalette(self):
        color_id = np.argmax(self._color_weights)
        palette_coordinate = self._color_coordinates[color_id]
        self._palette_coordinates.append(palette_coordinate)

        palette_color = self._rgb_colors[color_id]
        self._palette_colors.append(palette_color)
        return palette_coordinate

    def _updateWeight(self, palette_coordinate):
        dists = normVectors(self._color_coordinates - palette_coordinate)
        factors = 1.0 - np.exp(- dists ** 2 / (self._sigma ** 2))
        self._color_weights = factors * self._color_weights


## Palette selection plotter.
class PaletteSelectionPlot:
    ## Constructor
    #  @param palette_selection PaletteSelection instance for plotting.
    def __init__(self, palette_selection):
        self._palette_selection = palette_selection

    def paletteImage(self, size=16, spacing=4):
        palette_colors = self._palette_selection.paletteColors()
        num_colors = len(palette_colors)

        w = num_colors * size + (num_colors - 1) * spacing
        h = size

        palette_image = np.zeros((h, w, 4), dtype=np.float)

        for i, palette_color in enumerate(palette_colors):
            x_min = i * size + i * spacing
            x_max = x_min + size

            palette_image[:, x_min:x_max, 0:3] = palette_color
            palette_image[:, x_min:x_max, 3] = 1.0
        return palette_image

    def plot(self, plt):
        palette_image = self.paletteImage()
        plt.imshow(palette_image)

# -*- coding: utf-8 -*-
## @package palette.core.color_samples
#
#  Implementation of simple color sampling.
#  @author      tody
#  @date        2015/08/18

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from palette.cv.image import to32F, rgb
from palette.datasets.google_image import loadData


## Implementation of 3D color histograms.
class Hist3D:
    ## Constructor
    #  @param image          input image.
    #  @param num_bins       target number of histogram bins.
    #  @param alpha          low density clip.
    def __init__(self, image,
                 num_bins=16, alpha=0.3):
        self._pixels = self.toPixels(image)
        self._num_bins = num_bins
        self._alpha = alpha

        self.computeColorRanges()
        self.computeHistogram()

    def toPixels(self, image):
        if len(image.shape) == 2:
            h, w = image.shape
            return image.reshape((h * w))

        h, w, cs = image.shape
        return image.reshape((-1, cs))

    def computeColorRanges(self):
        pixels = self._pixels

        cs = pixels.shape[1]

        c_min = np.zeros(cs)
        c_max = np.zeros(cs)
        for ci in xrange(cs):
            c_min[ci] = np.min(pixels[:, ci])
            c_max[ci] = np.max(pixels[:, ci])

        self._color_ranges = [c_min, c_max]

    def computeHistogram(self):
        pixels = self._pixels
        num_bins = self._num_bins
        c_min, c_max = self._color_ranges

        hist_bins = np.zeros((num_bins, num_bins, num_bins), dtype = np.int32)

        num_pixels = pixels.shape[0]
        color_ids = (num_bins - 1) * (pixels - c_min) / (c_max-c_min)
        color_ids = np.int32(color_ids)

        for color_id in color_ids:
            hist_bins[color_id[0], color_id[1], color_id[2]] += 1

        self._hist_bins = hist_bins

    def colorIDs(self):
        density_mean = np.mean(self._hist_bins)
        color_ids = np.where(self._hist_bins > density_mean * self._alpha)
        return np.array(color_ids).T

    def colorSamples(self):
        color_ids = self.colorIDs()

        num_bins = self._num_bins
        c_min, c_max = self._color_ranges
        color_samples = c_min + (color_ids / (c_max - c_min)) / (num_bins - 1.0)
        color_samples = np.clip(color_samples, 0.0, 1.0)
        return color_samples

    def colorDensities(self):
        color_densities = np.float32(self._hist_bins[self.colorIDs().T])
        density_max = np.max(color_densities)
        color_densities = color_densities / density_max

        return color_densities

    def plotColorSamples(self, plt):
        color_ids = self.colorIDs()
        color_samples = self.colorSamples()
        density_size = self.plotDensitySize()

        plt.scatter(color_ids[:, 0], color_ids[:, 1], color_ids[:, 2],
                    color=color_samples, s=density_size)

    def plotDensitySize(self):
        color_densities = self.colorDensities()
        density_size = 10.0 * np.power(100.0, color_densities)
        return density_size


if __name__ == '__main__':
    C_8U = loadData(data_name="banana", i=3)
    rgb_8U = rgb(C_8U)
    C_32F = to32F(rgb_8U)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    hist3D = Hist3D(C_32F)
    hist3D.plotColorSamples(ax)

    plt.show()
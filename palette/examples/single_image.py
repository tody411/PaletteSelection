# -*- coding: utf-8 -*-
## @package palette.examples.single_image
#
#  Minimal example for single image.
#  @author      tody
#  @date        2015/08/29

from palette.io_util.image import loadRGB
from palette.core.hist_3d import Hist3D
from palette.core.palette_selection import PaletteSelection
import matplotlib.pyplot as plt

from palette.datasets.google_image import dataFile


image_file = dataFile("flower", 0)

# Load image.
image = loadRGB(image_file)

# 16 bins, Lab color space
hist3D = Hist3D(image, num_bins=16, color_space='Lab')

color_coordinates = hist3D.colorCoordinates()
color_densities = hist3D.colorDensities()
rgb_colors = hist3D.rgbColors()

# 5 colors from Lab color samples.
palette_selection = PaletteSelection(color_coordinates,
                                             color_densities, rgb_colors,
                                             num_colors=5, sigma=70.0)

fig = plt.figure()

# Plot image.
fig.add_subplot(131)
plt.imshow(image)
plt.axis('off')

# Plot palette colors.
fig.add_subplot(132)
palette_selection.plot(plt)
plt.axis('off')

# Plot 3D color histogram.
ax = fig.add_subplot(133, projection='3d')
hist3D.plot(ax)

plt.show()
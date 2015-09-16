
# -*- coding: utf-8 -*-
## @package palette.core.lab_slices
#
#  palette.core.lab_slices utility package.
#  @author      tody
#  @date        2015/09/15

import numpy as np
import matplotlib.pyplot as plt

from palette.cv.image import Lab2rgb


## OpenCV implementation of Lab2rgb
def Lab2rgb_cv(img):
    h, w = img.shape[:2]
    mask = 255 * np.ones((h, w), dtype=np.uint8)
    return Lab2rgb(img), mask


## Simple python implementation of Lab2rgb.
def Lab2rgb_py(img):
    XYZ = Lab2xyz(img)
    return xyz2rgb(XYZ)


## Convert Lab to XYZ.
def Lab2xyz(img):
    XYZ = np.zeros(img.shape)
    L, a, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    XYZ[:, :, 1] = (1.0 / 116.0) * (L + 16.0)
    XYZ[:, :, 0] = XYZ[:, :, 1] + (1.0 / 500.0) * a
    XYZ[:, :, 2] = XYZ[:, :, 1] - (1.0 / 200.0) * b

    def f(t):
        t_large = t > 6.0 / 29.0
        t_small = t <= 6.0 / 29.0

        t[t_large] = t[t_large] ** 3
        t[t_small] = (116.0 * t[t_small] - 16.0) * ((3.0 / 29.0) ** 3)
        return t

    XYZ[:, :, 0] = 0.95047 * f(XYZ[:, :, 0])
    XYZ[:, :, 1] = 1.00000 * f(XYZ[:, :, 1])
    XYZ[:, :, 2] = 1.08883 * f(XYZ[:, :, 2])
    return XYZ


## Convert XYZ to RGB.
def xyz2rgb(XYZ):
    RGB = np.zeros(XYZ.shape)

    RGB[:, :, 0] = 3.2410 * XYZ[:, :, 0] - 1.5374 * XYZ[:, :, 1] - 0.4986 * XYZ[:, :, 2]
    RGB[:, :, 1] = -0.9692 * XYZ[:, :, 0] + 1.8760 * XYZ[:, :, 1] + 0.0416 * XYZ[:, :, 2]
    RGB[:, :, 2] = 0.0556 * XYZ[:, :, 0] - 0.2040 * XYZ[:, :, 1] + 1.0570 * XYZ[:, :, 2]

    R, G, B = RGB[:, :, 0], RGB[:, :, 1], RGB[:, :, 2]
    mask = 255 * np.ones((R.shape), dtype=np.uint8)
    mask[R < 0.0] = 0
    mask[G < 0.0] = 0
    mask[B < 0.0] = 0
    mask[R > 1.0] = 0
    mask[G > 1.0] = 0
    mask[B > 1.0] = 0

    RGB[mask == 0, :] = 0.0

    return RGB, mask


## Implementation of Lab slice.
class LabSlice:
    ## Constructor
    #  @param a_range     range of a coordinate.
    #  @param b_range     range of b coordinate.
    #  @param size        output image size.
    #  @param func        Lab2rgb convert function.
    def __init__(self, a_range=[-127.0, 127.0], b_range=[127.0, -127.0], size=512, func=Lab2rgb_cv):
        self._size = size
        self._a_range = a_range
        self._b_range = b_range
        self._func = func

        self._createGrid()

    ## Return image size.
    def size(self):
        return self._size

    ## Return range of a coordinate.
    def aRange(self):
        return self._a_range

    ## Return range of b coordinate.
    def bRange(self):
        return self._b_range

    ## Return ab slice with mask.
    def slice(self, L):
        size = self._size
        slice_Lab = np.zeros((size, size, 3), dtype=np.float32)

        slice_Lab[:, :, 0] = L
        slice_Lab[:, :, 1] = self._a_grid
        slice_Lab[:, :, 2] = self._b_grid

        slice_rgb, mask = self._func(slice_Lab)
        return slice_rgb, mask

    ## Return xy coordinates for the given ab.
    def ab2xy(self, ab):
        a_min, a_max = self._a_range
        b_min, b_max = self._b_range
        x = (self._size - 1) * (ab[0] - a_min) / (a_max - a_min)
        y = (self._size - 1) * (ab[1] - b_min) / (b_max - b_min)

        return np.array([x, y])

    ## Create grid.
    def _createGrid(self):
        a_axis = np.linspace(self._a_range[0], self._a_range[1], self._size)
        b_axis = np.linspace(self._b_range[0], self._b_range[1], self._size)

        a_grid, b_grid = np.meshgrid(a_axis, b_axis)

        self._a_grid = a_grid
        self._b_grid = b_grid


## Plotter for Lab slice.
class LabSlicePlot:
    ## Constructor
    #  @param lab_slice   LabSlice.
    #  @param num_slices  number of slices for animation.
    #  @param num_ticks   number of ticks.
    def __init__(self, lab_slice, num_slices=51, num_ticks=10):
        self._lab_slice = lab_slice
        self._img_plot = plt.imshow(lab_slice.slice(0)[0])
        font_size = 15
        self._L_txt = plt.text(0, -2, '', fontsize=font_size)
        self._num_slices = num_slices
        self._Ls = np.linspace(0.0, 100.0, num_slices)
        self._num_ticks = num_ticks

        plt.xlabel("a")
        plt.ylabel("b")
        self._aTicks()
        self._bTicks()

    ## Plot.
    def plot(self, L):
        self._L_txt.set_text('L=%s' % L)
        slice = self._lab_slice.slice(L)[0]
        self._img_plot.set_array(slice)

    ## Animation function for matplot.
    def animationFunc(self, step, *args):
        L_id = step % self._num_slices
        L = self._Ls[L_id]
        self._L_txt.set_text('L=%s' % L)

        slice = self._lab_slice.slice(L)[0]
        self._img_plot.set_array(slice)

        return [self._L_txt, self._img_plot]

    def _aTicks(self):
        size = self._lab_slice.size()
        x_list = np.linspace(0, size - 1, self._num_ticks)
        a_range = self._lab_slice.aRange()
        a_list = np.int32(np.linspace(a_range[0], a_range[1], self._num_ticks))
        plt.xticks(x_list, a_list)

    def _bTicks(self):
        size = self._lab_slice.size()
        y_list = np.linspace(0, size - 1, self._num_ticks)
        b_range = self._lab_slice.bRange()
        b_list = np.int32(np.linspace(b_range[0], b_range[1], self._num_ticks))
        plt.yticks(y_list, b_list)

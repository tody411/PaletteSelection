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
from palette.cv.image import to32F
from palette.io_util.image import loadRGB
from palette.plot.window import showMaximize

_root_dir = os.path.dirname(__file__)


## Result directory for SOM results.
def resultDir():
    result_dir = os.path.abspath(os.path.join(_root_dir, "../results"))
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)
    return result_dir



def runPaletteSelectionResult(image_file):
    image_name = os.path.basename(image_file)
    image_name = os.path.splitext(image_name)[0]

    C_8U = loadRGB(image_file)
    C_32F = to32F(C_8U)

    fig = plt.figure(figsize=(10, 8))
    fig.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.95, wspace=0.05, hspace=0.05)
    plt.title("Automatic Color Palette Selection")
    plt.subplot(131)
    plt.title("%s" % (image_name))
    plt.imshow(C_32F)
    plt.axis('off')

    showMaximize()


def runPaletteSelectionResults(data_names, data_ids):
    for data_name in data_names:
        print "Palette Selection: %s" % data_name
        for data_id in data_ids:
            print "Data ID: %s" % data_id
            image_file = dataFile(data_name, data_id)
            runPaletteSelectionResult(image_file)


if __name__ == '__main__':
    data_names = ["apple", "tulip", "flower"]
    data_ids = [0, 1, 2]

    runPaletteSelectionResults(data_names, data_ids)


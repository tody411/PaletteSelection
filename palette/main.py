# -*- coding: utf-8 -*-
## @package palette.main
#
#  Main funcion.
#  @author      tody
#  @date        2015/08/20

from palette.datasets.google_image import createDatasets
from palette.core.palette_selection import runPaletteSelectionResults

if __name__ == '__main__':
    data_names = ["apple", "tulip", "flower"]
    num_images = 3
    data_ids = range(3)

    createDatasets(data_names, num_images, update=False)
    runPaletteSelectionResults(data_names, data_ids)

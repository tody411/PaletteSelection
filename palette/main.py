# -*- coding: utf-8 -*-
## @package palette.main
#
#  Main funcion.
#  @author      tody
#  @date        2015/08/20

from palette.datasets.google_image import createDatasets
from palette.results.single_image import signleImageResults
from palette.results.multi_images import multiImagesResults

if __name__ == '__main__':
    data_names = ["tulip", "flower"]
    num_images = 5
    data_ids = range(3)

    createDatasets(data_names, num_images, update=False)
    signleImageResults(data_names, data_ids)
    multiImagesResults(data_names, data_ids)

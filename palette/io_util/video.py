
# -*- coding: utf-8 -*-
## @package palette.io_util.video
#
#  palette.io_util.video utility package.
#  @author      tody
#  @date        2015/09/16


import cv2
from palette.cv.image import rgb2bgr


def saveVideo(file_path, images, fps=30, size=None):
    if size is None:
        h, w = images[0].shape[:2]
        size = (w, h)

        print size

    fourcc = cv2.cv.CV_FOURCC('W', 'M', 'V', '2')
    writer = cv2.VideoWriter(file_path, fourcc, fps, size, True)

    for image in images:
        bgr = rgb2bgr(image)
        writer.write(bgr)

    writer.release()

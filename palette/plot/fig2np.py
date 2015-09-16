
# -*- coding: utf-8 -*-
## @package palette.plot.fig2np
#
#  palette.plot.fig2np utility package.
#  @author      tody
#  @date        2015/09/16

import numpy as np


##  Convert matplot figure to numpy.array
def figure2numpy(fig, call_draw=True):
    if call_draw:
        fig.canvas.draw()

    fig_data = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
    image = fig_data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image

#!/usr/bin/env python

from mask import *
import gdsCAD
import utils

###########################################################################
#
# This codes demonstrates how to take a mask defined at the wafer
# scale and convert it to a 4-layer GCA mask for stepper 2.
#
###########################################################################


mask = Mask()
layered_mask = GCA200QuadrantMask()
mask.convertGDStoMask('gds/GDStoMaskTest.gds')
scaled_mask = layered_mask.convertWaferScaleMask(mask)
scaled_mask.save('Sample Masks/GDStoMaskTest5x.gds')



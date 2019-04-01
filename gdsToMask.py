from mask import *
import gdsCAD
import utils

mask = Mask()
layered_mask = GCA200QuadrantMask()
mask.convertGDStoMask('/Users/liamcohen/Desktop/GDStoMaskTest.gds')
scaled_mask = layered_mask.convertWaferScaleMask(mask)
scaled_mask.save('/Users/liamcohen/Desktop/GDStoMaskTest5x.gds')



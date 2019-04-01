from mask import *
import gdsCAD
import utils


##########################################################################
# Setup basic mask with 4 quadrants and add global/local alignment marks #
##########################################################################

mask = GCA200QuadrantMask()
mask.addAlignmentMark(type='global', position=(-17000, -17000), layer=1, dieStep=9.6)
mask.addAlignmentMark(type='local', position=(-18000, -18000), layer=1, dieStep=9.6)

####################################################################
# Define a few basic elements, such as top and bottom gates        #
####################################################################

def get_bottom_gate_pointset(lattice_size):
    return [(100, 100), (100, -100), (30, -100), (30, -500 - 150), (-270 + 100, -500 - 150), (-270 + 100, -700), (-290 + 100, -700),
            (-290 + 100, -875), (-298 + 100, -875), (-298 + 100, -900), (-300 + 100 + lattice_size/2.0, -900), (-300 + 100 + lattice_size/2.0, -900 - lattice_size),
            (-300 + 100 - lattice_size/2.0, -900 - lattice_size), (-300 + 100 - lattice_size/2.0, -900), (-302 + 100, -900),
            (-302 + 100, -875), (-310 + 100, -875), (-310 + 100, -700), (-330 + 100, -700), (-330 + 100, -440 - 150), (-30, -440 - 150), (-30, -100), (-100, -100), (-100, 100)]


####################################################################
# Add bottom gate to lower right hand corner                       #
####################################################################

bottom_gate_cell_tot = gdsCAD.core.Cell("bottom_gate_cell_ref")

for i in range(2):
    bottom_gate = gdsCAD.core.Boundary(get_bottom_gate_pointset(5*(i+1))).scale(k=5)
    bottom_gate_cell_i = gdsCAD.core.Cell("bottom_gate_cell_i")
    bottom_gate_cell_i.add(bottom_gate)

    bottom_gate_cell_ref_i = gdsCAD.core.CellReference(bottom_gate_cell_i, origin = (21000*i, 0))
    bottom_gate_cell_tot.add(bottom_gate_cell_ref_i)

bottom_gate_cell_tot_ref = gdsCAD.core.CellArray(ref_cell=bottom_gate_cell_tot, rows=2, cols=1, spacing=(0, 21000), origin=(-9500, -6000))

mask.addToQuadrant("lower_right", bottom_gate_cell_tot_ref)

####################################################################
# Add test spot to lower right hand corner                         #
####################################################################
test_box = gdsCAD.shapes.Rectangle((-300, -300), (300, 300), layer=1)
test_box_cell = gdsCAD.core.Cell("text_box_cell")
test_box_cell.add(test_box)
test_box_cell_ref = gdsCAD.core.CellReference(test_box_cell, origin=(1000, 1000))

mask.addToQuadrant("lower_right", test_box_cell_ref)

####################################################################
# Add test spot to lower left hand corner                         #
####################################################################
test_box = gdsCAD.shapes.Rectangle((-300, -300), (300, 300), layer=1)
test_box_cell = gdsCAD.core.Cell("text_box_cell")
test_box_cell.add(test_box)
test_box_cell_ref = gdsCAD.core.CellReference(test_box_cell, origin=(1300, 1000))

mask.addToQuadrant("lower_left", test_box_cell_ref)

####################################################################
# Add top gate to lower left hand corner                           #
####################################################################

top_gate_cell_tot = gdsCAD.core.Cell("top_gate_cell_ref")

for i in range(2):
    top_gate = gdsCAD.core.Boundary(get_bottom_gate_pointset(6*(i+1))).scale(k=5).reflect(axis='y')
    top_gate_cell_i = gdsCAD.core.Cell("top_gate_cell_i")
    top_gate_cell_i.add(top_gate)

    top_gate_cell_ref_i = gdsCAD.core.CellReference(top_gate_cell_i, origin = (21000*i, 0))
    top_gate_cell_tot.add(top_gate_cell_ref_i)

top_gate_cell_tot_ref = gdsCAD.core.CellArray(ref_cell=top_gate_cell_tot, rows=2, cols=1, spacing=(0, 21000), origin=(-11500, -6000))
mask.addToQuadrant("lower_left", top_gate_cell_tot_ref)


####################################################################
# Define EBL alignment marks                                       #
####################################################################
ebl_quadrant_alignment_mark_points = [(5, 500), (5, 5), (500, 5), (500, -5), (5, -5), (5, -500), (-5, -500), (-5, -5),
                                      (-500, -5), (-500, 5), (-5, 5), (-5, 500)]

ebl_quadrant_alignment_mark = gdsCAD.core.Boundary(ebl_quadrant_alignment_mark_points)
ebl_quadrant_alignment_mark_cell = gdsCAD.core.Cell("quadrant_alignment_marks")
ebl_quadrant_alignment_mark_cell.add(ebl_quadrant_alignment_mark)
ebl_quadrant_alignment_marks = gdsCAD.core.CellArray(ref_cell=ebl_quadrant_alignment_mark_cell, rows=3, cols=3, spacing=(15000, 15000), origin=(-15000, -15000))
ebl_quadrant_alignment_marks = ebl_quadrant_alignment_marks

ebl_alignment_mark_points = [(8, 1), (-1, 1), (-1, -8), (1, -8), (1, -1), (8, -1)]
ebl_alignment_mark = gdsCAD.core.Boundary(ebl_alignment_mark_points)

ebl_alignment_mark_cell_ur = gdsCAD.core.Cell("alignment_mark_cell_ur")
ebl_alignment_mark_cell_br = gdsCAD.core.Cell("alignment_mark_cell_br")
ebl_alignment_mark_cell_bl = gdsCAD.core.Cell("alignment_mark_cell_bl")
ebl_alignment_mark_cell_ul = gdsCAD.core.Cell("alignment_mark_cell_ul")

ebl_alignment_mark_ur = ebl_alignment_mark.copy().rotate(angle=-90).scale(k=5)
ebl_alignment_mark_br = ebl_alignment_mark.copy().rotate(angle=-180).scale(k=5)
ebl_alignment_mark_bl = ebl_alignment_mark.copy().rotate(angle=-270).scale(k=5)
ebl_alignment_mark_ul = ebl_alignment_mark.copy().scale(k=5)

ebl_alignment_mark_cell_ur.add(ebl_alignment_mark_ur)
ebl_alignment_mark_cell_br.add(ebl_alignment_mark_br)
ebl_alignment_mark_cell_bl.add(ebl_alignment_mark_bl)
ebl_alignment_mark_cell_ul.add(ebl_alignment_mark_ul)

ebl_alignment_mark_cell_ref_ur = gdsCAD.core.CellReference(ebl_alignment_mark_cell_ur, origin=(125, 125))
ebl_alignment_mark_cell_ref_br = gdsCAD.core.CellReference(ebl_alignment_mark_cell_br, origin=(125, -125))
ebl_alignment_mark_cell_ref_bl = gdsCAD.core.CellReference(ebl_alignment_mark_cell_bl, origin=(-125, -125))
ebl_alignment_mark_cell_ref_ul = gdsCAD.core.CellReference(ebl_alignment_mark_cell_ul, origin=(-125, 125))

ebl_alignment_marks_cell = gdsCAD.core.Cell("ebl_alignment_marks_cell")
ebl_alignment_marks_cell.add(ebl_alignment_mark_cell_ref_ur)
ebl_alignment_marks_cell.add(ebl_alignment_mark_cell_ref_br)
ebl_alignment_marks_cell.add(ebl_alignment_mark_cell_ref_bl)
ebl_alignment_marks_cell.add(ebl_alignment_mark_cell_ref_ul)
ebl_alignment_marks_cell_ref = gdsCAD.core.CellArray(ref_cell=ebl_alignment_marks_cell, rows=2, cols=2,
                                                     spacing=(21000, 21000), origin=(-10500, -10525))

mask.addToQuadrant("upper_right", ebl_alignment_marks_cell_ref)
mask.addToQuadrant("upper_right", ebl_quadrant_alignment_marks)

####################################################################
# Define Complementary EBL alignment marks                         #
####################################################################
cebl_alignment_mark_cell_ref_ur = gdsCAD.core.CellReference(ebl_alignment_mark_cell_bl, origin=(125, 125))
cebl_alignment_mark_cell_ref_br = gdsCAD.core.CellReference(ebl_alignment_mark_cell_ul, origin=(125, -125))
cebl_alignment_mark_cell_ref_bl = gdsCAD.core.CellReference(ebl_alignment_mark_cell_ur, origin=(-125, -125))
cebl_alignment_mark_cell_ref_ul = gdsCAD.core.CellReference(ebl_alignment_mark_cell_br, origin=(-125, 125))

cebl_alignment_marks_cell = gdsCAD.core.Cell("cebl_alignment_marks_cell")
cebl_alignment_marks_cell.add(cebl_alignment_mark_cell_ref_ur)
cebl_alignment_marks_cell.add(cebl_alignment_mark_cell_ref_br)
cebl_alignment_marks_cell.add(cebl_alignment_mark_cell_ref_bl)
cebl_alignment_marks_cell.add(cebl_alignment_mark_cell_ref_ul)
cebl_alignment_marks_cell_ref = gdsCAD.core.CellArray(ref_cell=cebl_alignment_marks_cell, rows=2, cols=2,
                                                     spacing=(21000, 21000), origin=(-10500, -10525))

mask.addToQuadrant("lower_right", cebl_alignment_marks_cell_ref)

####################################################################
# Define Nabity alignment markers                                  #
####################################################################

nabity_alignment_mark_cell = gdsCAD.core.Cell("nabity_alignment_mark_cell")
square = gdsCAD.shapes.Rectangle(point1=(-7.5, -7.5), point2=(7.5, 7.5))
square_cell = gdsCAD.core.Cell("square_cell")
square_cell.add(square)

square_ref_1 = gdsCAD.core.CellReference(square_cell, origin=(-7.5, -7.5))
square_ref_2 = gdsCAD.core.CellReference(square_cell, origin=(7.5, 7.5))
nabity_alignment_mark_cell.add(square_ref_1)
nabity_alignment_mark_cell.add(square_ref_2)

nabity_alignment_mark_array = gdsCAD.core.CellArray(ref_cell=nabity_alignment_mark_cell, rows=2, cols=2,
                                                     spacing=(70*5, 70*5))
nabity_alignment_mark_array_cell = gdsCAD.core.Cell("nabity_alignment_mark_array_cell")
nabity_alignment_mark_array_cell.add(nabity_alignment_mark_array)

nabity_alignment_marks = gdsCAD.core.CellArray(ref_cell=nabity_alignment_mark_array_cell, rows=2, cols=2,
                                               spacing=(21000, 21000), origin=(-10675, -10700))

mask.addToQuadrant("upper_left", nabity_alignment_marks)

####################################################################
# Define Define device contacts                                    #
####################################################################
contact_base_angle_pointset_1 = [(-45 - 50, 32.5), (-635 + 525, 32.5), (-635, 510), (-800, 510), (-800, 700), (-1000, 700), (-1000, 500), (-800, 500),
                               (-645, 500), (-645 + 525, 26.5), (-45 - 50, 26.5)]

contact_base_angle_pointset_2 = [(-45 - 50, 19.5), (-665 + 525, 19.5), (-665, 210), (-800, 210), (-800, 400), (-1000, 400), (-1000, 200), (-800, 200),
                                 (-675, 200), (-675 + 525, 12.5), (-45 - 50, 12.5)]

contact_base_angle_1 = gdsCAD.core.Boundary(contact_base_angle_pointset_1)
contact_base_angle_2 = gdsCAD.core.Boundary(contact_base_angle_pointset_2)

contact_base_straight_pointset = [(-45 - 50, 5.5), (-800, 5.5), (-800, 100), (-1000, 100), (-1000, -100), (-800, -100), (-800, -5.5), (-45 - 50, -5.5)]
contact_base_straight = gdsCAD.core.Boundary(contact_base_straight_pointset)

contacts_base_cell = gdsCAD.core.Cell("contact_base_cell")
contacts_base_cell.add(contact_base_straight.copy().scale(k=5))
contacts_base_cell.add(contact_base_angle_1.copy().scale(k=5))
contacts_base_cell.add(contact_base_angle_2.copy().scale(k=5))
contacts_base_cell.add(contact_base_straight.copy().reflect(axis="x").scale(k=5))
contacts_base_cell.add(contact_base_angle_1.copy().reflect(axis="x").scale(k=5))
contacts_base_cell.add(contact_base_angle_2.copy().reflect(axis="x").scale(k=5))

contacts_base_cell.add(contact_base_straight.copy().reflect(axis="y").scale(k=5))
contacts_base_cell.add(contact_base_angle_1.copy().reflect(axis="y").scale(k=5))
contacts_base_cell.add(contact_base_angle_2.copy().reflect(axis="y").scale(k=5))
contacts_base_cell.add(contact_base_straight.copy().reflect(axis="y").reflect(axis="x").scale(k=5))
contacts_base_cell.add(contact_base_angle_1.copy().reflect(axis="y").reflect(axis="x").scale(k=5))
contacts_base_cell.add(contact_base_angle_2.copy().reflect(axis="y").reflect(axis="x").scale(k=5))

contacts_base_cell.add(contact_base_straight.copy().rotate(angle=90).scale(k=5))
contacts_base_cell.add(contact_base_angle_1.copy().rotate(angle=90).scale(k=5))
contacts_base_cell.add(contact_base_angle_2.copy().rotate(angle=90).scale(k=5))
contacts_base_cell.add(contact_base_straight.copy().reflect(axis="x").rotate(angle=90).scale(k=5))
contacts_base_cell.add(contact_base_angle_1.copy().reflect(axis="x").rotate(angle=90).scale(k=5))
contacts_base_cell.add(contact_base_angle_2.copy().reflect(axis="x").rotate(angle=90).scale(k=5))

contacts = gdsCAD.core.CellArray(ref_cell=contacts_base_cell, rows=2, cols=2, spacing=(21000, 21000), origin=(-10500, -10525))
mask.addToQuadrant("upper_left", contacts)

####################################################################
# Define top gate overlap                                          #
####################################################################
top_gate_overlap_pointset = [(100, 100), (100, -100), (30, -100), (30, -500 - 150), (-270 + 100, -500 - 150), (-270 + 100, -700), (-290 + 100, -700),
                             (-330 + 100, -700), (-330 + 100, -440 - 150), (-30, -440 - 150), (-30, -100), (-100, -100), (-100, 100)]

top_gate_overlap = gdsCAD.core.Boundary(top_gate_overlap_pointset).scale(k=5).reflect(axis="y")
top_gate_overlap_cell = gdsCAD.core.Cell("top_gate_overlap")
top_gate_overlap_cell.add(top_gate_overlap)

top_gate_overlap_array = gdsCAD.core.CellArray(top_gate_overlap_cell, rows=2, cols=2, spacing=(21000, 21000), origin=(-11500, -6000))
mask.addToQuadrant("upper_left", top_gate_overlap_array)

####################################################################
# Save Mask to Desktop                                             #
####################################################################
mask.save('~/Desktop/SuperlatticeOpticalMaskV6.gds')

####################################################################
# Create Waferscale Mask and add EBL Pattern                       #
####################################################################
wafer_mask = mask.makeWaferScaleGDS(precision=0.125E-9)

#70 nm pitch square lattice
hole_36nm = gdsCAD.shapes.Disk((0, 0), 0.0365/2, layer=2)
hole_cell_70nm = gdsCAD.core.Cell("hole")
hole_cell_70nm.add(hole_36nm)

hole_cell_70nm_array_A = gdsCAD.core.CellArray(ref_cell=hole_cell_70nm, rows=90, cols=115, spacing=(0.070, 0.070),
                                        origin=(-2104, -2106))
hole_cell_70nm_array_B = gdsCAD.core.CellArray(ref_cell=hole_cell_70nm, rows=90, cols=115, spacing=(0.070, 0.070),
                                        origin=(-2104, 2094))
hole_cell_70nm_array_C = gdsCAD.core.CellArray(ref_cell=hole_cell_70nm, rows=180, cols=200, spacing=(0.070, 0.070),
                                        origin=(2093, 2088))
hole_cell_70nm_array_D = gdsCAD.core.CellArray(ref_cell=hole_cell_70nm, rows=180, cols=200, spacing=(0.070, 0.070),
                                        origin=(2093, -2112))

wafer_mask['TOP'].add(hole_cell_70nm_array_A)
wafer_mask['TOP'].add(hole_cell_70nm_array_B)
wafer_mask['TOP'].add(hole_cell_70nm_array_C)
wafer_mask['TOP'].add(hole_cell_70nm_array_D)

#Add dose marks to show EBL development prior to etching
ebl_dose_mark_points = [(8, 1), (-1, 1), (-1, -8), (1, -8), (1, -1), (8, -1)]
ebl_dose_mark = gdsCAD.core.Boundary(ebl_dose_mark_points, layer=2)

ebl_dose_mark_br_cell = gdsCAD.core.Cell("ebl_dose_mark_br_cell")
ebl_dose_mark_br_cell.add(ebl_dose_mark.copy().rotate(angle=180))

ebl_dose_mark_ul_cell = gdsCAD.core.Cell("ebl_dose_mark_ul_cell")
ebl_dose_mark_ul_cell.add(ebl_dose_mark.copy())

ebl_dose_mark_br_cellref = gdsCAD.core.CellReference(ebl_dose_mark_br_cell.copy(), origin=(15, -15))
ebl_dose_mark_ul_cellref = gdsCAD.core.CellReference(ebl_dose_mark_ul_cell.copy(), origin=(-15, 15))

ebl_dose_mark_cell = gdsCAD.core.Cell(name="dose_mark_cell_ws")
ebl_dose_mark_cell.add(ebl_dose_mark_br_cellref)
ebl_dose_mark_cell.add(ebl_dose_mark_ul_cellref)

ebl_dose_mark_cellarray = gdsCAD.core.CellArray(ebl_dose_mark_cell, rows=2, cols=2, spacing=(4200, 4200), origin=(-2100, -2106))

wafer_mask['TOP'].add(ebl_dose_mark_cellarray)

wafer_mask.save('~/Desktop/WaferScale.gds')

##########
mask = Mask()
layered_mask = GCA200QuadrantMask()
mask.convertGDStoMask('/Users/liamcohen/Desktop/GDStoMaskTest.gds')
layered_mask.convertWaferScaleMask(mask)


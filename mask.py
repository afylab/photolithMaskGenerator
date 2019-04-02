import gdsCAD
import utils

#########################################################################################################
# Module Name:  Mask.py
# Project:      Photolithography Mask Generator
# Copyright (c) Young Lab - 2019

# Description: To Be Written

# THIS CODE AND INFORMATION IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND,
# EITHER EXPRESSED OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND/OR FITNESS FOR A PARTICULAR PURPOSE.
#########################################################################################################

class Mask(gdsCAD.core.Layout):
    def __init__(self, name='Mask', precision=1E-9):
        '''
         Mask object which is a subclass of the Layout object, automatically add a single top cell.
         Takes two initialization variables, 'name' and 'precision.'  Name is a string which assigns a name
         to the underlying gdsCAD Layout object behind this blank mask.  'Precision' sets the numerical precision
         of the GDS layout.  Typically this will not need to be changed from its default value, but it may be necessary
         for fracturing high precision e-beam lithography gds files.
        '''

        super(Mask, self).__init__(name=name, precision=precision)
        top_cell = gdsCAD.core.Cell('TOP')
        self.add(top_cell)

    def convertGDStoMask(self, directory):
        '''
         This function takes as input a string pointing to the directory of a GDS file.  It then takes that file
         and adds the contents of that gds file, layer by layer, into the currently instantiated Mask object.

        :param directory: String pointing to GDS file directory
        :return: None
        '''
        layout = gdsCAD.core.GdsImport(directory)
        if len(layout.top_level()) > 1:
            raise(UserWarning("GDSII file has more than 1 distinct top-level cell, unable to import."))
        else:
            self['TOP'] = layout.top_level()[0].copy('TOP')


class GCA200Mask(Mask):
    def __init__(self):
        '''
         Subclass of Mask object.

         This Mask is designed to be compatible with stepper two, i.e., GCA200 -- automatically adds reticle alignment
         marks, plus the available writable window.  It is useful to note that although patterns can be written anywhere
         inside of the GCA alignment mark bounding box, stepper 2 has a 21mm diameter aperture (at
         wafer scale), which means that the maximum exposable die size is 14.8mm x 14.8mm.
        '''

        super(GCA200Mask, self).__init__()

        # Add reticle layout to mask
        for cell_name, cell in gdsCAD.core.GdsImport('gds/OpticalMaskTemplate2.gds').iteritems():
            if cell_name in self.keys():
                self[cell_name] = cell
            else:
                self.add(cell)

    def convertGDStoMask(self, directory):
        '''
         This function takes as input a string pointing to the directory of a GDS file.  It then takes that file
         and adds the contents of that mask, layer by layer, into the currently instantiated Mask object.

        :param directory: String pointing to GDS file directory
        :return: None
        '''
        layout = gdsCAD.core.GdsImport(directory)
        if len(layout.top_level()) > 1:
            raise(UserWarning("GDSII file has more than 1 distinct top-level cell, unable to import."))
        else:
            self['TOP'].add(layout.top_level()[0].copy('IMPORT_MASK_TOP'))

    def DRCCheck(self):
        '''

         :return: Boolean -- true if all elements in mask follow design rule check for stepper 2
        '''
        raise(NotImplementedError)


class GCA200QuadrantMask(GCA200Mask):
    def __init__(self):
        '''
          Initialize mask with 4 workable quadrants, i.e., four subcells that fit in each corner
          of the layout file.  This mask is designed to contain multiple photolithography layers
          so I will implement a few helper functions that will be useful for doing multiple layer
          masks.
        '''

        super(GCA200QuadrantMask, self).__init__()

        #add bounding box visual aid
        bounding_box = gdsCAD.shapes.Rectangle((-37100, -37100), (37100, 37100), layer=2)
        self['TOP'].add(bounding_box)

        #add quadrant 1 -- upper left hand corner
        self['TOP'].add(gdsCAD.core.CellReference(gdsCAD.core.Cell("upper_left"), origin=(-18550, 18550)))

        #add quandrant 2 -- upper right hand corner
        self['TOP'].add(gdsCAD.core.CellReference(gdsCAD.core.Cell("upper_right"), origin=(18550, 18550)))

        #add quadrant 3 -- lower right hand corner
        self['TOP'].add(gdsCAD.core.CellReference(gdsCAD.core.Cell("lower_right"), origin=(18550, -18550)))

        #add quadrant 4 -- lower left hand corner
        self['TOP'].add(gdsCAD.core.CellReference(gdsCAD.core.Cell("lower_left"), origin=(-18550, -18550)))

        self.quadrant_names = {"upper_left", "upper_right", "lower_right", "lower_left"}


    def convertWaferScaleMask(self, mask, layers = [1, 2, 3, 4]):
        '''
         Takes a Mask object (at wafer scale) as input and then moves the specified layers into the correct
         quadrants.  This will be most useful for designing patterns at the wafer scale, and then quickly
         producing a 5x times scaled up optical mask with the layers oriented correctly.

         layers[0] --> upper right
         layers[1] --> lower right
         layers[2] --> lower left
         layers[3] --> upper left

         :param mask: Mask Object -- gds file with pattern at wafer scale
         :param layers: List -- list of layer id numbers that map to mask quadrants
         :return: None
        '''
        num_to_layer_dict = {layers[0]:"upper_right", layers[1]:
            "lower_right", layers[2]:"lower_left", layers[3]:"upper_left"}

        def add_and_scale_cell(cell):
            scaled_cell = gdsCAD.core.Cell(cell.name)
            if len(cell.objects) > 0:
                for object in cell.objects:
                    scaled_cell.add(object.scale(k=5))
                for dep_cell in cell.references:
                    scaled_cell.add(add_and_scale_cell(dep_cell))

            return scaled_cell

        def add_cell_objects(cell, layered_mask):
            for object in cell.objects:
                object_cell = gdsCAD.core.Cell("container_cell")
                object_cell.add(object)
                layered_mask.addToQuadrant(num_to_layer_dict[object.layer], object_cell)
            for reference in cell.references:
                add_cell_objects(reference, layered_mask)

        top_cell = add_and_scale_cell(mask['TOP'])
        scaled_mask = GCA200QuadrantMask()
        add_cell_objects(top_cell, scaled_mask)

        return scaled_mask

    def getCellReference(self, cell, reference_name):
        '''
         Return CellReference matching reference_name, if none found return False

         :param cell: cell object to search for CellReference: gdsCAD.core.Cell()
         :param reference_name: name of cell reference -- String
         :return: CellReference object
        '''
        for reference in cell.references:
            if reference.ref_cell.name == reference_name:
                return reference
        return False

    def getCellFromReference(self, reference_name):
        '''
         Get cell from reference name, this function returns the cell corresponding to the
         CellReference object with a given name.

         :param reference_name: String
         :return: gdsCAD.core.Cell()
        '''
        for reference in self['TOP'].references:
            if reference.ref_cell.name == reference_name:
                return reference.ref_cell
        return False

    def addToQuadrant(self, quadrant, cell):
        '''
         Add cell or cell reference to quadrant

         :param qudrant: name of quadrant to add to -- String
         :param cell: cell or cell reference to add to quadrant cell
         :return: None
        '''
        if quadrant not in self.quadrant_names:
            raise("Error, not a valid quadrant name!")
        else:
            self.getCellReference(self['TOP'], quadrant).ref_cell.add(cell)


    def makeWaferScaleGDS(self, precision=1E-9):
        '''
         Produces a new mask object at wafer scale with each layer overlaid with each other.
         This helps check for layer-layer alignment and can also help produce gds files which
         can be edited for other other fab processes such as the EBL.

         :param precision: Precision of GDS layout for returned mask
         :return: Mask Object
        '''

        wafer_scale_mask = Mask(name=self.name+'_ws', precision=precision)

        for quadrant in self.quadrant_names:
            quadrant_elements = [element.scale(k=0.2) for element in self.getCellFromReference(quadrant).flatten()]
            for quadrant_element in quadrant_elements:
                boundary_cell = gdsCAD.core.Cell("boundary")
                boundary_cell.add(quadrant_element)
                wafer_scale_mask['TOP'].add(boundary_cell)

        return wafer_scale_mask



    def addAlignmentMark(self, type='global', quadrant='upper_right', standardKeys=True, dieStep=7.692, aperture=63.5, position=(0, 0), layer=1):
        '''
         This method will add standard global or local alignment marks to one of the four quadrants.  If standardKeys is set
         to true, the method will add two alignment marks spaced appropriately such that standardKeys on the stepper
         can be used

         :param type: determines the type of alignment mark to be placed [options - 'global' or 'local'] -- String
         :param quadrant: quadrant where alignment marks should appear -- String
         :param dieStep: die step in mm is the x-spacing between dies used to calculated spacing between alignment marks when standardKeys is set to true -- ignored otherwise -- Integer
         :param aperture: spacing between objectives on stepper -- Integer
         :param standardKeys: boolean variable to set or unset use of standard key alignment -- boolean
         :param position: position of first alignment mark relative to quadrant center -- (x, y) integer tuple
         :return: None
        '''

        alignment_mark_string = 'gds/DFAS_AlignmentMark.gds' if type == 'local' else 'gds/GlobalAlignmentMarks.gds'
        alignment_mark_layer = 2 if type == 'local' else 1
        alignment_mark_name = 'DFAS_SOLID_POS' if type == 'local' else 'TOP'
        alignment_mark_layout = gdsCAD.core.GdsImport(alignment_mark_string, layers={alignment_mark_layer:layer})
        alignment_cell = alignment_mark_layout[alignment_mark_name].copy("AlignmentMark")

        if quadrant not in self.quadrant_names:
            raise("Error, not a valid quadrant name!")
        else:
            if standardKeys:
                spacing = int(round(5000 * (aperture - dieStep * int(aperture/dieStep))))

                alignment_mark_ref_main = gdsCAD.core.CellReference(alignment_cell, origin=position)
                alignment_mark_ref_align = gdsCAD.core.CellReference(alignment_cell, origin=(position[0] + spacing, position[1]))

                self.getCellReference(self['TOP'], quadrant).ref_cell.add(alignment_mark_ref_main)
                self.getCellReference(self['TOP'], quadrant).ref_cell.add(alignment_mark_ref_align)
            else:
                alignment_mark_ref = gdsCAD.core.CellReference(alignment_cell, origin=position)
                self.getCellReference(alignment_mark_layout['TOP'], quadrant).add(alignment_mark_ref)








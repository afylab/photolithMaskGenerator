import gdsCAD

def inBoundingBox(point, bounding_box):
    '''
     Check if given point is in within a given bounding box

     :param point
     :param bounding_box:
     :return:
    '''
    if point[0] > bounding_box[0][0] and point[0] < bounding_box[1][0] and point[1] > bounding_box[0][1] and point[1] > bounding_box[1][1]:
        return True
    else:
        return False

def getAllElementsInLayer(cell, layer):
    '''
     This function returns a list of all the elements that lie in a given cell, recursively
     that also lie in a layer specified.

     :param cell:
     :return:
    '''
    def filter_by_layer(objects, layer_in):
        filtered_list = []

        for i in range(len(objects)):
            if objects[i].layer == layer_in:
                filtered_list.append(objects[i])

        return tuple(filtered_list)


    def get_objects_in_cell_by_layer(inp):
        if len(inp.references) == 0:
            return filter_by_layer(inp.objects, layer)
        else:
            addition_list = ()
            for reference in inp.references:
                addition_list += get_objects_in_cell_by_layer(reference.ref_cell)

            return filter_by_layer(inp.objects, layer) + addition_list

    return get_objects_in_cell_by_layer(cell)


def makeEBLAlignmentMarksBasic(rows=159, columns=159, row_spacing=300, column_spacing=300):
    '''
     This function returns a cell reference containing an array of cross-shaped alignment marks
     with a given spacing in x and y.  One can also define how many rows and columns to write.

     :param rows:
     :param columns:
     :param row_spacing:
     :param column_spacing:
     :return:
    '''

    #Define Cell to return
    alignmentMarkCell = gdsCAD.core.Cell("alignmentMarkCell")

    #Define basic cross
    cross_points = [[-1*5, 6*5], [1*5, 6*5], [1*5, 1*5], [6*5, 1*5], [6*5, -1*5],
              [1*5, -1*5], [1*5, -6*5], [-1*5, -6*5], [-1*5, -1*5], [-6*5, -1*5],
              [-6*5, 1*5], [-1*5, 1*5]]

    cross_polygon = gdsCAD.core.Boundary(cross_points, layer=0, datatype=0)
    cross_cell = gdsCAD.core.Cell("single_cross")
    cross_cell.add(cross_polygon)

    #define alignment mark array
    for i in range(rows):
        for j in range(columns):
            total_cell_ref = gdsCAD.core.CellReference(cross_cell, origin=(i*row_spacing, j*column_spacing))
            alignmentMarkCell.add(total_cell_ref)

    return gdsCAD.core.CellReference(alignmentMarkCell, origin=(-23000, -23000))

def makeEBLAlignmentMarksQRCodes(rows = 159, columns = 159, row_spacing = 300, column_spacing = 300, layer=4):
    '''

     :param rows:
     :param colums:
     :param row_spacing:
     :param column_spacing:
     :return:
    '''

    circle = gdsCAD.shapes.Disk((0, 0), 5, layer=layer)
    circle_cell = gdsCAD.core.Cell("circle_cell")
    circle_cell.add(circle)

    mark0 = gdsCAD.shapes.Rectangle((-5, -2.5), (5, 2.5), layer=layer)
    mark0_cell = gdsCAD.core.Cell("mark0")
    mark0_cell.add(mark0)
    mark0_ref = gdsCAD.core.CellReference(mark0_cell, origin=(-25, 40))

    mark1 = gdsCAD.shapes.Rectangle((-2.5, -2.5), (2.5, 2.5), layer=layer)
    mark1_cell = gdsCAD.core.Cell("mark1")
    mark1_cell.add(mark1)
    mark1_ref = gdsCAD.core.CellReference(mark1_cell, origin=(-10, 40))

    qr_codes = gdsCAD.core.Cell("qr_codes")

    qr_code_positions_rows = [(5*4.5, 5*1.5), (5*1.5, 5*1.5), (-5*1.5, 5*1.5), (-5*4.5, 5*1.5), (5*4.5, 5*4.5), (5*1.5, 5*4.5), (-5*1.5, 5*4.5), (-5*4.5, 5*4.5)]
    qr_code_positions_columns = [(5*4.5, -5*4.5), (5*1.5, -5*4.5), (-5*1.5, -5*4.5), (-5*4.5, -5*4.5), (5*4.5, -5*1.5), (5*1.5, -5*1.5), (-5*1.5, -5*1.5), (-5*4.5, -5*1.5)]

    #for now I'm going to hard code in what spaces to avoid:


    #define qr code array:
    for i in range(rows):
        for j in range(columns):
            qr_cell = gdsCAD.core.Cell("qr_cell")
            qr_cell.add(mark1_ref)
            qr_cell.add(mark0_ref)

            row_bin = format(i, '08b')
            column_bin = format(j, '08b')

            for k, position in enumerate(row_bin[::-1]):
                if int(position):
                    qr_cell.add(gdsCAD.core.CellReference(circle_cell, origin=qr_code_positions_rows[k]))

            for l, position1 in enumerate(column_bin[::-1]):
                if int(position1):
                    qr_cell.add(gdsCAD.core.CellReference(circle_cell, origin=qr_code_positions_columns[l]))

            qr_codes.add(gdsCAD.core.CellReference(qr_cell, origin=(j*column_spacing, i*row_spacing)))

    return gdsCAD.core.CellReference(qr_codes, origin = (-rows*row_spacing/2.0, -columns*column_spacing/2))

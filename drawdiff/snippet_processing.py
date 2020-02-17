import xml.etree.ElementTree as ET

class Legend:

    def __init__(self, legend_name):
        self.legend = ET.parse(f"drawdiff/xml_snippets/{legend_name}.xml")

    def paste_id_into_legend(self, action, elements):
        #TODO: need to adjust legend size according to 'id' lines
        root = self.legend.getroot()
        ids_elem = root.find(f".//mxCell[@fill_this=\"true\"]")
        ids_elem.attrib['value'] += f"\n{action}"
        for elem in elements:
            ids_elem.attrib['value'] += f"\n{elem.attrib['id']}"
    
    def put_legend_into_diagram(self, root_elem):
        x, y = self.get_coordinates_for_legend(root_elem)
        for elem in self.legend.iter('mxGeometry'):
            if 'x' in elem.attrib and 'y' in elem.attrib:
                elem.attrib['x'] = str(float(elem.attrib['x']) + x)
                elem.attrib['y'] = str(float(elem.attrib['y']) + y)
        for elem in self.legend.iter('mxPoint'):
            if 'x' in elem.attrib and 'y' in elem.attrib:
                elem.attrib['x'] = str(float(elem.attrib['x']) + x)
                elem.attrib['y'] = str(float(elem.attrib['y']) + y)

        mx_cell_root = root_elem.find('.//root')
        for elem in self.legend.iter('mxCell'):
            if elem.attrib['id'] != '0' and elem.attrib['id'] != '1':
                mx_cell_root.append(elem)
            else:
                continue

    def get_coordinates_for_legend(self, root_elem):
        max_x = None
        max_y = None
        for elem in root_elem.iter('mxGeometry'):
            if 'x' in elem.attrib and 'y' in elem.attrib:
                if max_x == None or float(elem.attrib['x']) > max_x:
                    max_x = float(elem.attrib['x'])
                if  max_y == None or float(elem.attrib['y']) < max_y:
                    max_y = float(elem.attrib['y'])
        #TODO: optimize these two loops 
        for elem in root_elem.iter('mxPoint'):
            if 'x' in elem.attrib and 'y' in elem.attrib:
                if max_x == None or float(elem.attrib['x']) > max_x:
                    max_x = float(elem.attrib['x'])
                if max_y == None or float(elem.attrib['y']) < max_y:
                    max_y = float(elem.attrib['y'])
        return max_x, max_y

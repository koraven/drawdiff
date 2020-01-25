import xml.etree.ElementTree as ET


def process_legend():
    tree = ET.parse('drawdiff/xml_snippets/legend.xml')
    root = tree.getroot()
    for child in root.iter('mxCell'):
        print(child.attrib['value'])

process_legend()
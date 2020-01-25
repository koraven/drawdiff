import xml.etree.ElementTree as ET
from drawdiff.compare_xml import xml_compare
from drawdiff.decompress import decompress_xml
import drawdiff.confluence as confluence
import drawdiff.showdiff as sd
import sys
import argparse


def main():

    parser = argparse.ArgumentParser(description='Compare drawio xmls. Example: python main.py -l old.xml new.xml')
    parser.add_argument('-l', '--local', dest='local', action='store_true', default=False, help='local files or confluence attachments. DEFAULT: confluence')
    parser.add_argument('-t', '--title', dest='title', action='store')
    parser.add_argument('objects', metavar='O', type=str, nargs='+', help='Objects to compare: numbers of versions for confluence, files for local mode.')
    args = parser.parse_args()
    
    if args.local:
        tree_old = ET.parse(str(args.objects[0]))
        tree_new = ET.parse(str(args.objects[1]))
        root1 = tree_old.getroot()
        root2 = tree_new.getroot()
    else:
        root1 = ET.fromstring(confluence.get_diagram_from_attachments(
                                page_title=args.title, 
                                version=str(args.objects[0]))
                                )
        root2 = ET.fromstring(confluence.get_diagram_from_attachments(
                                page_title=args.title, 
                                version=str(args.objects[1]))
                                )
    
    try:
        decompress_xml(root1)
    except ValueError:
        print('diagram 1 is not compressed')
    try:
        decompress_xml(root2)
    except ValueError:
        print('diagram 2 is not compressed')    
    
    updated_elements = []
    deleted_elements = []
    new_elements = []

    for child_of_old in root1.iter('mxCell'):
        child_of_new = root2.find(f".//mxCell[@id=\"{child_of_old.attrib['id']}\"]")
        if child_of_new == None:
            deleted_elements.append(child_of_old)
            continue
        if not xml_compare(child_of_old,child_of_new):
            updated_elements.append(child_of_new)

    for child_of_new in root2.iter('mxCell'):
        child_of_old = root1.find(f".//mxCell[@id=\"{child_of_new.attrib['id']}\"]")
        if child_of_old == None:
            new_elements.append(child_of_new)

    print('updated')
    for child in updated_elements:
        sd.highlight_diff(child.attrib)
        print(child.attrib['id'])
    print('deleted:')
    for child in deleted_elements:
        mx_cell_root = root2.find('.//root')
        sd.highlight_diff(child.attrib,'delete')
        mx_cell_root.append(child)
        print(child.attrib['id'])
    print('added:')
    for child in new_elements:
        sd.highlight_diff(child.attrib,'add')
        print(child.attrib['id'])
    with open('test_web.xml','w') as f:
        f.write(ET.tostring(root2,encoding="unicode"))

if __name__ == '__main__':
    main()
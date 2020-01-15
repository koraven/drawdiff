import xml.etree.ElementTree as ET
from lib.compare_xml import xml_compare
from lib.decompress import decompress_xml
from lib.confluence import get_diagram_from_attachments
import sys
import argparse

def replace_gradient(attribs,action='update'):
    color = '#FF00FF'
    if action == 'delete':
        color = '#333333'
    elif action == 'add':
        color = '#00FF00'
    if 'style' in attribs:
        if 'edge' not in attribs:
            if 'image;' in attribs['style']:
                attribs['style'] += f"imageBorder={color};strokeWidth=5;"
            elif 'gradientColor' in attribs['style']:
                attribs['style'] = attribs['style'].replace('gradientColor=none',f"gradientColor={color}")
            else:
                attribs['style'] = attribs['style'] + f"gradientColor={color};"
            
            if 'fillColor' not in attribs['style']:
                attribs['style'] = attribs['style'] + 'fillColor=#FFFFFF'
            elif 'fillColor=none' in attribs['style']:
                attribs['style'] = attribs['style'].replace('fillColor=none',f"fillColor=#FFFFFF")
            
            if 'shape' not in attribs['style']:
                if 'strokeOpacity=0;' in attribs['style']:
                    attribs['style'] = attribs['style'].replace('strokeOpacity=0;','')
                    if 'strokeColor=none' in attribs['style']:
                        attribs['style'] = attribs['style'].replace('strokeColor=none',f"strokeColor={color}")
                    else:
                        attribs['style'] += f"strokeColor=#{color}"
#TODO: add diff for lines(edge=1) 
#        else:
#            if 'strokeColor' in attribs
#            attribs['style']

def main():

    parser = argparse.ArgumentParser(description='Compare drawio xmls')
    parser.add_argument('-l', '--local', dest='local', action='store_true', default=False, help='local files or confluence attachments. DEFAULT: confluence')
    parser.add_argument('-t', '--title', dest='title', action='store')
    parser.add_argument('objects', metavar='O', type=str, nargs='+', help='Objects to compare: numbers of versions for confluence, files for local mode.')
    args = parser.parse_args()
    
    if args.local:
        #tree_old = ET.parse('STG-17.xml')
        #tree_new = ET.parse('STG-18.xml')
        tree_old = ET.parse(str(args.objects[0]))
        tree_new = ET.parse(str(args.objects[1]))
        root1 = tree_old.getroot()
        root2 = tree_new.getroot()
    else:
        root1 = ET.fromstring(get_diagram_from_attachments(
                                page_title=args.title, 
                                version=str(args.objects[0]))
                                )
        root2 = ET.fromstring(get_diagram_from_attachments(
                                page_title=args.title, 
                                version=str(args.objects[1]))
                                )
    
    try:
        decompress_xml(root1)
    except ValueError:
        print('diagram 1 was not compressed')
    try:
        decompress_xml(root2)
    except ValueError:
        print('diagram 2 was not compressed')    
    
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
        replace_gradient(child.attrib)
        print(child.attrib['id'])
    print('deleted:')
    for child in deleted_elements:
        mx_cell_root = root2.find('.//root')
        replace_gradient(child.attrib,'delete')
        mx_cell_root.append(child)
        print(child.attrib['id'])
    print('added:')
    for child in new_elements:
        replace_gradient(child.attrib,'add')
        print(child.attrib['id'])
    #tree_new.write('test_output2.xml')
    with open('test_web.xml','w') as f:
        f.write(ET.tostring(root2,encoding="unicode"))

if __name__ == '__main__':
    main()
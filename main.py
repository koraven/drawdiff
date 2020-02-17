import xml.etree.ElementTree as ET
from drawdiff.compare_xml import xml_compare
from drawdiff.decompress import decompress_xml
import drawdiff.confluence as confluence
import drawdiff.showdiff as sd
import drawdiff.snippet_processing as legend
import sys
import argparse


def main():

    parser = argparse.ArgumentParser(description='Compare drawio xmls. Example: python main.py -l old.xml new.xml')
    parser.add_argument('-l', '--local', dest='local', action='store_true', default=False, help='local files or confluence attachments. DEFAULT: confluence')
    parser.add_argument('-t', '--title', dest='title', action='store', help='Title of Confluence page')
    parser.add_argument('-o', '--output',dest='output',action='store', help='Output file')
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
    my_legend = legend.Legend('legend')
    #TODO: Replace it with an approach without exceptions
    try:
        decompress_xml(root1)
    except ValueError:
        pass
    try:
        decompress_xml(root2)
    except ValueError:
        pass 
    
    updated_elements = {}
    deleted_elements = []
    new_elements = []
    #compare all elements of old tree with elements of new tree to find updated and deleted elements
    for child_of_old in root1.iter('mxCell'):
        child_of_new = root2.find(f".//mxCell[@id=\"{child_of_old.attrib['id']}\"]")
        if child_of_new == None:
            deleted_elements.append(child_of_old)
            continue
        if child_of_old.attrib['id']=='-QjtrjUzRDEMRZ5MF8oH-25':
            print('qwe')
        changed, elem_subtype = xml_compare(child_of_old,child_of_new)
        if changed:
            updated_elements[child_of_new] = elem_subtype
    #compare all elements of new tree with elements of old tree to find added elements
    for child_of_new in root2.iter('mxCell'):
        child_of_old = root1.find(f".//mxCell[@id=\"{child_of_new.attrib['id']}\"]")
        if child_of_old == None:
            new_elements.append(child_of_new)

    for child, elem_subtype in updated_elements.items():
        sd.highlight_diff(child.attrib,'update',elem_subtype=elem_subtype)
    for child in deleted_elements:
        mx_cell_root = root2.find('.//root')
        sd.highlight_diff(child.attrib,'delete')
        mx_cell_root.append(child)
    for child in new_elements:
        sd.highlight_diff(child.attrib,'add')

    my_legend.paste_id_into_legend("Updated:", updated_elements)
    my_legend.paste_id_into_legend("Deleted:", deleted_elements)
    my_legend.paste_id_into_legend("Added:", new_elements)
    my_legend.put_legend_into_diagram(root2)

    if args.output:
        with open(args.output,'w') as f:
            f.write(ET.tostring(root2,encoding="unicode"))
    #TODO: Fix
    #else:
    #    print(ET.tostring(root2,encoding="unicode"))

if __name__ == '__main__':
    main()
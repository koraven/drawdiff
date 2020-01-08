from lxml import etree
from xmldiff import main, formatting
import xml.etree.ElementTree as ET


formatter = formatting.XMLFormatter()
diff = main.diff_files(left='old.xml',right='new.xml',formatter=formatter,
diff_options={'uniqueattrs': ['id'],'F': 0.98})
with open('test.xml','w') as f:
    f.write(diff)

tree = ET.parse('test.xml')
root = tree.getroot()
#=root.getchildren()
#b=list(root)
def replace_gradient(attribs):
    if 'style' in attribs and 'edge' not in attribs:
        if 'image;' in attribs['style']:
            attribs['style'] += 'imageBorder=#FF00FF;strokeWidth=5;'
        elif 'gradientColor' in attribs['style']:
            attribs['style'] = attribs['style'].replace('gradientColor=none','gradientColor=#FF00FF')
        else:
            attribs['style'] = attribs['style'] + 'gradientColor=#FF00FF;'
        #print(attribs)

for child in root.iter('mxCell'):
    changed = False
    elements_to_delete = []
    for gch in child.iter():
#        if 'id' in gch.attrib and 'ZSwEeQw7avFoCkHJYFPM-46' == gch.attrib['id']:
#            print('qwe')
        if gch.tag == '{http://namespaces.shoobx.com/diff}insert':
            changed = True
        if '{http://namespaces.shoobx.com/diff}update-attr' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}update-attr')
        if '{http://namespaces.shoobx.com/diff}add-attr' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}add-attr')
        if '{http://namespaces.shoobx.com/diff}move-node' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}move-node')
        if '{http://namespaces.shoobx.com/diff}insert' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}insert')
        if '{http://namespaces.shoobx.com/diff}delete' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}delete')    
        if '{http://namespaces.shoobx.com/diff}delete-attr' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}delete-attr')
        if '{http://namespaces.shoobx.com/diff}rename' in gch.attrib:
            changed = True
            gch.attrib.pop('{http://namespaces.shoobx.com/diff}rename')
    if changed:
        replace_gradient(child.attrib)
for child in root.iter():
    for gch in child.findall('{http://namespaces.shoobx.com/diff}delete'):
        child.remove(gch)
    for gch in child.findall('{http://namespaces.shoobx.com/diff}insert'):
        child.remove(gch)
            
tree.write('test_output.xml')
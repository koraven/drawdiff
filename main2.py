
import xml.etree.ElementTree as ET

tree_old = ET.parse('old.xml')
tree_new = ET.parse('new.xml')

root1 = tree_old.getroot()
root2 = tree_new.getroot()



def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

def xml_compare(x1, x2, reporter=None):
#    if x1.tag != x2.tag:
#        if reporter:
#            reporter('Tags do not match: %s and %s' % (x1.tag, x2.tag))
#        return False
    for name, value in x1.attrib.items():
        if x2.attrib.get(name) != value:
            if reporter:
                reporter('Attributes do not match: %s=%r, %s=%r'
                         % (name, value, name, x2.attrib.get(name)))
            return False
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            if reporter:
                reporter('x2 has an attribute x1 is missing: %s'
                         % name)
            return False
    if not text_compare(x1.text, x2.text):
        if reporter:
            reporter('text: %r != %r' % (x1.text, x2.text))
        return False
    if not text_compare(x1.tail, x2.tail):
        if reporter:
            reporter('tail: %r != %r' % (x1.tail, x2.tail))
        return False
    cl1 = list(x1)
    cl2 = list(x2)
    if len(cl1) != len(cl2):
        if reporter:
            reporter('children length differs, %i != %i'
                     % (len(cl1), len(cl2)))
        return False
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        if not xml_compare(c1, c2, reporter=reporter):
            if reporter:
                reporter('children %i do not match: %s'
                         % (i, c1.tag))
            return False
    return True

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
#        else:
#            if 'strokeColor' in attribs
#            attribs['style']

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
tree_new.write('test_output2.xml')
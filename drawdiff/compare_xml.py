
def text_compare(t1, t2):
    if not t1 and not t2:
        return True
    if t1 == '*' or t2 == '*':
        return True
    return (t1 or '').strip() == (t2 or '').strip()

def xml_compare(x1, x2):
#    if x1.tag != x2.tag:
#        if reporter:
#            reporter('Tags do not match: %s and %s' % (x1.tag, x2.tag))
#        return False
    for name, value in x1.attrib.items():
        if name == 'parent':
            continue
        if x2.attrib.get(name) != value:
            if name == 'value':
                return True, 'value'
            return True, None
    for name in x2.attrib.keys():
        if name not in x1.attrib:
            return True, None
    if not text_compare(x1.text, x2.text):
        return True, 'text'
    if not text_compare(x1.tail, x2.tail):
        return True, 'tail'
    cl1 = list(x1)
    cl2 = list(x2)
    if len(cl1) != len(cl2):
        return True, None
    i = 0
    for c1, c2 in zip(cl1, cl2):
        i += 1
        changed, elem_subtype = xml_compare(c1, c2)
        if changed:
            return True, elem_subtype
    return False, None

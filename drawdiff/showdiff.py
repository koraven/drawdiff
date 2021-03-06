import re

def get_color(action):
    corr_table = {
        'update': '#FF00FF',
        'delete': '#000000',
        'add': '#00FF00'
    }
    return corr_table[action]

def get_opacity(action):
    corr_table = {
        'update': '100',
        'delete': '50',
        'add': '100'
    }
    return corr_table[action]

def get_elem_type(attribs):
    if 'style' in attribs:
        if 'edge' not in attribs:
            if 'image;' in attribs['style']:
                return 'image'
            if 'text;' in attribs['style']:
                return 'text'
            if 'shape' in attribs['style']:
                return 'shape'
        if 'edge' in attribs and attribs['edge'] == '1':
            return 'edge'
        elif 'strokeOpacity=0;' in attribs['style']:
            return 'group'

#TODO: if necessary combine these methods in the future
def change_style(attribs, **kwargs):
    if 'style' in attribs:
        for k, v in kwargs.items():
            if k not in attribs['style']:
                attribs['style'] += f";{k}={v};"
            else:
                regexp = f"{k}=[#]?\w*;"
                attribs['style'] = re.sub(regexp,f"{k}={v};",attribs['style'])
#TODO: if necessary combine these methods in the future
#add **kwargs to provide capability of changing existing text attributes
def change_value(attribs, text_to_add):
    if 'value' not in attribs:
        attribs['value'] = ''
    if attribs['value'] == '':
        attribs['value'] = text_to_add
    else:
        attribs['value'] += f"  {text_to_add}"

def highlight_diff(attribs,action,elem_subtype=None):
    color = get_color(action)
    opacity = get_opacity(action)
    elem_type = get_elem_type(attribs)
    
    if elem_subtype == 'value':
        change_value(attribs,f"<font style=\"font-size: 8px;background-color: rgb(255 , 0 , 255)\">CHANGED_VALUE</font>")
    if elem_type == 'image':
        change_style(attribs,imageBorder=color,strokeWidth=7)
    if elem_type == 'text':
        change_style(attribs, strokeColor=color,strokeOpacity=100)
    elif elem_type == 'group':
        change_style(attribs,strokeOpacity='100',strokeColor=color)
    elif elem_type == 'edge':
        if action == 'delete' or action == 'add':
            change_style(attribs, strokeColor=color, opacity=opacity, strokeWidth='10',dashed='1')
        else:
            change_style(attribs, strokeColor=color, opacity=opacity, strokeWidth='10')
    else:
        change_style(attribs,gradientColor=color,fillColor=color, opacity=opacity)
    #this code adds ids of changed elements to make possible searching with legend
    change_value(attribs, f"<font style=\"font-size: 1px\">{attribs['id']}</font>" )

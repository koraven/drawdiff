import zlib
import base64
from urllib.parse import unquote
import xml.etree.ElementTree as ET

def decode_base64_and_inflate( b64string ):
    decoded_data = base64.b64decode( b64string )
    return zlib.decompress( decoded_data, -15)

def deflate_and_base64_encode( string_val ):
    zlibbed_str = zlib.compress( string_val )
    compressed_string = zlibbed_str[2:-4]
    return base64.b64encode( compressed_string )

def decompress_xml(root):
    for diagram in root.iter('diagram'):
        b64_text = diagram.text
        try:
            decomp_text = unquote(decode_base64_and_inflate(b64_text).decode())
        except:
            raise ValueError
        parsed_diagram = ET.fromstring(decomp_text)
        diagram.text = '\n   '
        diagram.append(parsed_diagram)          
    return True


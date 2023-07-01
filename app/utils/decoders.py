from urllib.parse import parse_qs
import base64

def decode_base64(encoded_string):
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')  # Decode to string using appropriate encoding
    return decoded_string

def decode_form_url_encoded(body):
    decoded_data = parse_qs(body)
    decoded_dict = {}

    for key, value in decoded_data.items():
        if len(value) == 1:
            decoded_dict[key] = value[0]
        else:
            decoded_dict[key] = value

    return decoded_dict    
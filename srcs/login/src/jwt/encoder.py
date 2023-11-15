import base64
import json


class Base64Encoder:
    def __init__(self):
        pass

    @staticmethod
    def encode(obj) -> str:
        if isinstance(obj, str):
            s = obj
        else:
            s = json.dumps(obj)
        base64_encoded = base64.b64encode(s.encode('utf-8'))
        return Base64Encoder.replace_special_characters(base64_encoded.decode('utf-8'))

    @staticmethod
    def replace_special_characters(s: str) -> str:
        substitutions = {
            '=': '',
            '+': '-',
            '/': '_'
        }
        for char_to_be_replaced in substitutions:
            s = s.replace(char_to_be_replaced, substitutions[char_to_be_replaced])
        return s

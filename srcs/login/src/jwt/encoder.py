import base64
import json


class Base64Encoder:
    def __init__(self):
        pass

    @staticmethod
    def encode(obj):
        return base64.urlsafe_b64encode(obj).rstrip(b'=')

    @staticmethod
    def decode(obj):
        padding = b'=' * (4 - (len(obj) % 4))
        return base64.urlsafe_b64decode(obj.encode('utf-8') + padding)
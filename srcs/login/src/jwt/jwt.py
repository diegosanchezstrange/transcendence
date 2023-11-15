import base64
import json
import hmac

from config import Config
from encoder import Base64Encoder


class JWT:
    def __init__(self) -> None:
        self.config = Config()
        self.headers = Base64Encoder.encode(self.config.headers)
        self.payload = Base64Encoder.encode(self.config.payload)
        self.signature = self.create_signature('secret')
        self.all = f"{self.headers}.{self.payload}.{self.signature}"
        # print(self.headers)
        # print(self.payload)
        # print(self.config.payload)

    def __str__(self) -> str:
        return self.all

    def create_signature(self, secret: str) -> str:
        algo = self.config.algo[self.config.headers["alg"]]
        signature = hmac.new(secret.encode('utf-8'), f"{self.headers}.{self.payload}".encode('utf-8'), digestmod=algo)
        signature_base4 = base64.b64encode(signature.digest()).decode('utf-8')
        return Base64Encoder.replace_special_characters(signature_base4)


myjwt = JWT()
print(myjwt)
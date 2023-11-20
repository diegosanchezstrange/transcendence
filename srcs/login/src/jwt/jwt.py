import base64
import hashlib
import json
import hmac

from encoder import Base64Encoder


class JWT:
    def __init__(self, payload: dict) -> None:
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        self.headers = Base64Encoder.encode(json.dumps(headers).encode('utf-8'))
        self.payload = Base64Encoder.encode(json.dumps(payload).encode('utf-8'))
        self.signature = self.create_signature('secret')
        self.all = self.headers + b'.' + self.payload + b'.' + self.signature
        self.all = self.all.decode('utf-8')

    def __str__(self) -> str:
        return self.all

    def create_signature(self, secret: str) -> str:
        signature = hmac.new(secret.encode('utf-8'), self.headers + b'.' + self.payload, hashlib.sha256)
        signature = Base64Encoder.encode(signature.digest())
        return signature

    @staticmethod
    def decode_jwt(jwt_token: str, secret):
        encoded_header, encoded_payload, encoded_signature = jwt_token.split('.')

        header = json.loads(Base64Encoder.decode(encoded_header).decode('utf-8'))
        payload = json.loads(Base64Encoder.decode(encoded_payload).decode('utf-8'))
        signature = Base64Encoder.decode(encoded_signature)

        expected_signature = hmac.new(
            secret.encode('utf-8'), encoded_header.encode('utf-8') + b'.'
            + encoded_payload.encode('utf-8'), hashlib.sha256
        )
        if not hmac.compare_digest(signature, expected_signature.digest()):
            raise ValueError("Invalid signature")

        return payload


myjwt = JWT({
    "sub": "1234567890",
    "name": "John Doe",
    "iat": 1516239022
})
token = str(myjwt)
print(JWT.decode_jwt(token, 'secret'))
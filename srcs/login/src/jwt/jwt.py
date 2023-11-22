import os
import hashlib
import json
import hmac

from encoder import Base64Encoder


class JWT:
    class NoSecretFoundError(Exception):
        """This exception is raised in case there is no JWT_SECRET environment variable found"""
        def __init__(self):
            super().__init__('No JWT_SECRET environment variable found')

    class InvalidJwtTokenError(Exception):
        """This exception is raised in case the presented JWT is not valid"""
        def __init__(self):
            super().__init__('Invalid JWT Token')

    def __init__(self, payload: dict) -> None:
        headers = {
            "alg": "HS256",
            "typ": "JWT"
        }
        self.headers = Base64Encoder.encode(json.dumps(headers).encode('utf-8'))
        self.payload = Base64Encoder.encode(json.dumps(payload).encode('utf-8'))
        self.__secret = os.getenv('JWT_SECRET')
        if not self.__secret:
            raise JWT.NoSecretFoundError
        self.signature = self.create_signature(self.__secret)
        self.all = self.headers + b'.' + self.payload + b'.' + self.signature
        self.all = self.all.decode('utf-8')

    def __str__(self) -> str:
        return self.all

    def create_signature(self, secret: str) -> str:
        signature = hmac.new(secret.encode('utf-8'), self.headers + b'.' + self.payload, hashlib.sha256)
        signature = Base64Encoder.encode(signature.digest())
        return signature

    @staticmethod
    def decode_jwt(jwt_token: str):
        encoded_header, encoded_payload, encoded_signature = jwt_token.split('.')

        payload = json.loads(Base64Encoder.decode(encoded_payload).decode('utf-8'))
        signature = Base64Encoder.decode(encoded_signature)
        secret = os.getenv('JWT_SECRET')

        expected_signature = hmac.new(
            secret.encode('utf-8'), encoded_header.encode('utf-8') + b'.'
            + encoded_payload.encode('utf-8'), hashlib.sha256
        )
        if not hmac.compare_digest(signature, expected_signature.digest()):
            raise JWT.InvalidJwtTokenError()

        return payload


if __name__ == "__main__":
    """
    If you are using this to test my JWT class, please do not forget to export the 'JWT_TOKEN' environment var
    """

    try:
        myjwt = JWT({
            "sub": "testing stuff",
            "name": "ft_transcendence user",
            "iat": 2024
        })
    except JWT.NoSecretFoundError as e:
        print(e)
        exit(1)
    token = str(myjwt)
    print(f"JWT token: {token}")
    print(f"JWT token decoded: {JWT.decode_jwt(token)}")

import json

class Config:
    def __init__(self, file_name="config/config.json") -> None:
        self.file = file_name
        self.data = self.read_data()
        self.headers = self.data.get("headers")
        self.payload = self.data.get("payload")

        self.algo = {
            "HS256": "sha256"
        }

    def read_data(self) -> dict:
        with open(self.file, "r") as file:
            return json.loads(file.read())

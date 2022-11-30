from dotenv import dotenv_values


class Config:
    def __init__(self):
        self.env = dotenv_values(".env")


config = Config()

from dotenv import dotenv_values

options = {
    "STATE_QUERY_LIMIT": 25,
}


class Settings:
    def __init__(self):
        for key, value in [*dotenv_values().items(), *options.items()]:
            setattr(self, key, value)


IMG_TYPE = [
    "image/gif",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/x-icon",
    "image/tiff",
]

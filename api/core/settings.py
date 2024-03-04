from dotenv import dotenv_values

# add new or override .env variables from here
options = {
    "STATE_QUERY_LIMIT": 25,
}


class SettingsClass:
    def __init__(self):
        for key, value in [*dotenv_values().items(), *options.items()]:
            setattr(self, key, value)


Settings = SettingsClass()
DATABASE_URL = f"{Settings.DB_CONNECTION}://{Settings.DB_USERNAME}:{Settings.DB_PASSWORD}@{Settings.DB_HOST}:{Settings.DB_PORT}/{Settings.DB_DATABASE}"  # type: ignore
# print(DATABASE_URL)


IMG_TYPE = [
    "image/gif",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/x-icon",
    "image/tiff",
]

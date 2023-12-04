from dotenv import dotenv_values

# add new or override .env variables from here
options = {
    "STATE_QUERY_LIMIT": 25,
}


class Settings:
    def __init__(self):
        for key, value in [*dotenv_values().items(), *options.items()]:
            setattr(self, key, value)


st = Settings()
DATABASE_URL = f"{st.DB_CONNECTION}://{st.DB_USERNAME}:{st.DB_PASSWORD}@{st.DB_HOST}:{st.DB_PORT}/{st.DB_DATABASE}"  # type: ignore
# print(DATABASE_URL)


IMG_TYPE = [
    "image/gif",
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/x-icon",
    "image/tiff",
]

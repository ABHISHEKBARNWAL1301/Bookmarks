from pydantic_settings import BaseSettings


class Settings(BaseSettings):
# COCKROACHDB_PASSWORD=CyBZdjzf4G-kxCQ0u7QH5A
# COCKROACHDB_USER=abhishekbarnwal1301
# COCKROACHDB_NAME=bookmarkdb
# WIKIPEDIA_API_URL=https://en.wikipedia.org/w/api.php
# LLM_API_KEY=AIzaSyB56gI3cFOg0dY3y5EEFpBX18qsHUwYQHg
# LLM_MODEL=gemini-1.5-flash
# SECRET_KEY = "your_secret_key"    # Secret key for JWT encoding and decoding (store this securely)
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30


    cockroachdb_user: str
    cockroachdb_password: str
    cockroachdb_name: str
    wikipedia_api_url: str
    llm_api_key: str
    llm_model: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    


    class Config:
        env_file = ".env"


settings = Settings()

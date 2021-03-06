import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("API_TOKEN_MAIN")

admins = [
    os.getenv("Nikita_ID"),
]

ip = os.getenv("ip")


COD_CHAT_ID = -1001152933021

# DATABASE
DATABASE = os.getenv('DATABASE')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# PSN
PSN_EMAIL = os.getenv('PSN_EMAIL')
PSN_PASSWORD = os.getenv('PSN_PASSWORD')
PSN_USERNAME = os.getenv('PSN_USERNAME')

POSTGRES_URI = f'postgresql+asyncpg://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

if __name__ == '__main__':
    print(admins)
    print(ip)
    print(BOT_TOKEN)
    print(PSN_EMAIL)
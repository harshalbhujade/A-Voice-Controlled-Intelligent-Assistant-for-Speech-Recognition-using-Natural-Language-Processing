# todo: Add your api key here

from dotenv import load_dotenv
import os

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")
news_api = os.getenv("NEWS_API_KEY")

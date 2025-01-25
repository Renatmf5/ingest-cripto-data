from dotenv import load_dotenv
import os

# Load the environment variables
load_dotenv()

# Binance Keys
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")


import os
import dotenv as de

## load_dotenv() searches for .env file with environment variables
## os.getenv() get the variables names

de.load_dotenv()

PORT=os.getenv("PORT")
DB_NAME=os.getenv("DB_NAME")
DB_HOST=os.getenv("DB_HOST")
DB_PORT=os.getenv("DB_PORT")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
SECRET_KEY=os.getenv("SECRET_KEY")
from dotenv import load_dotenv
load_dotenv()
from app import create_app
import os


app, celery = create_app()

if __name__ == "__main__":
    port = os.getenv("PORT")
    app.run("localhost",port=int(port))
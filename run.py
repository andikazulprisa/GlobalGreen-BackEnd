from dotenv import load_dotenv
load_dotenv()

from app import create_app
from flask_migrate import upgrade
import logging

app = create_app()


with app.app_context():
    try:
        upgrade()
        print("Database migration successful.")
    except Exception as e:
        print("Database migration failed:", str(e))
        logging.exception("Migration error")

if __name__ == "__main__":
    app.run()

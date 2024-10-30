import os
from dotenv import load_dotenv
from flask_cors import CORS
from app.routes import app


load_dotenv()
app.config.from_object(os.getenv('CONFIG_ENV'))
app_access_url = app.config.get('APP_ACCESS_URL')
CORS(app, origins=[app_access_url])

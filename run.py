import os
from app import app, db
from dotenv import load_dotenv
from app.constants import ENV_LOCATION
from socket import gethostname
#----------------------------------------
# launch
#----------------------------------------

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	if 'liveconsole' not in gethostname(): #liveconsole is for the pythonanywhere deployment
		load_dotenv(ENV_LOCATION)
		port = int(os.getenv("PORT"))
		host = os.getenv("HOST")
		app.run(host=host, port=port)

import os
from dotenv import load_dotenv
from app.constants import ENV_LOCATION

load_dotenv(ENV_LOCATION)

class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = False
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = os.getenv('SECRET_KEY')
	CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///application.db'
	SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevelopmentConfig(Config):
	DEBUG = True

class ProductionConfig(Config):
	''' Configuration for deploying to pythonanywhere '''
	SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{hostname}/{databasename}"\
		.format(
			username=os.getenv('PRODUCTION_USERNAME'), # The username from the 'Databases' tab
			password=os.getenv('PRODUCTION_PASSWORD'), # The password you set on the 'Databases' tab,
			hostname=os.getenv('PRODUCTION_HOSTNAME'), # The database host address from the 'Databases' tab,
			databasename=os.getenv('PRODUCTION_DATABASENAME') # The database name
		)
	SQLALCHEMY_POOL_RECYCLE = 280
	SQLALCHEMY_POOL_TIMEOUT = 20
	SQLALCHEMY_POOL_PRE_PING = True
	SQLALCHEMY_ENGINE_OPTIONS = {
		'pool_recycle': SQLALCHEMY_POOL_RECYCLE,
		'pool_timeout': SQLALCHEMY_POOL_TIMEOUT,
		'pool_pre_ping': SQLALCHEMY_POOL_PRE_PING
	}
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	REDIS_URL = "redis://:{password}@{host}:{port}/0"\
	.format(
		password=os.getenv('REDIS_PASSWORD'), # On cloud: Configuration > Security
		host=os.getenv('REDIS_HOST'),
		port=os.getenv('REDIS_PORT')
	)

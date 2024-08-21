# Badam Satti
Flask server for Badam Satti App

## Requirements

Python 3.8.5+

## Server configuration files

All project configurations are in [`configuration.py`](app/configuration.py)

All game constants are in [`constants.py`](app/constants.py)


## Local server installation and setup

First, clone this repository.
```bash
git clone https://github.com/Sanvit-Katrekar/badam-7
cd badam-7
```

Install all necessary libraries:

```bash
pip install -r requirements.txt
```

Create a .env file and put in the following variables:
```env
PORT=xxxxx
HOST=xxxxx
SECRET_KEY=xxxxx
```
Run the application by running the `run.py` file:

```bash
python run.py
```
To see the application, access `http://{YOUR_HOST_HERE}:{YOUR_PORT_HERE}` in your browser.

> Note: The development server uses an sqlite3 database, but can be changed in [`configuration.py`](app/configuration.py)

## Server deployment to pythonanywhere

On your account at [pythonanywhere.com](pythonanywhere.com), 

Create a bash consolve and clone this repository.
```bash
git clone https://github.com/Sanvit-Katrekar/badam-7
cd badam-7
```

Add your web app in the `Web` section.

Create a MySQL database in the `Databases` section.

Then, make the following changes:

Create a `.env` file in repo,
> More precisely, the absolute path will be `/home/{YOUR_USERNAME}/{PATH_TO_CLONED_REPO}/.env`  
If required, this can be changed in [`constants.py`](app/constants.py)

And put in the following variables in the `.env`:
```env
SECRET_KEY=xxxxx
PRODUCTION_USERNAME=xxxxx
PRODUCTION_PASSWORD=xxxx
PRODUCTION_HOSTNAME=xxxx
PRODUCTION_DATABASENAME=xxxx
```
1. `SECRET_KEY`: Flask app secret key

2. `PRODUCTION_USERNAME`: The username you set from the 'Databases' tab in pythonanywhere

3. `PRODUCTION_PASSWORD`: The password you set from the 'Databases' tab

4. `PRODUCTION_HOSTNAME`: The database host address you set from the 'Databases' tab

5. `PRODUCTION_DATABASENAME`: The name of the database you set

Next, navigate to [`__init__.py`](app/__init__.py) and make the following comment changes to use the server's production configuration:

```python
app.config.from_object('app.configuration.ProductionConfig')
#app.config.from_object('app.configuration.DevelopmentConfig')
```

In the `Web` section, 

1. Change Source Code location to `/home/{YOUR_USERNAME}/{PATH_TO_CLONED_REPO}`
2. `Web` section, click on the `WSGI configuration file` and paste in the below code:

```python
# In file /var/www/{YOUR_USERNAME}_pythonanywhere_com_wsgi.py
import sys

# add your project directory to the sys.path
project_home = '/home/{YOUR_USERNAME}/{PATH_TO_GIT_REPO}'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from app import app as application  # noqa
```

Next, run the `run.py` file to initialize the database
```bash
python run.py
```

Now one last thing:

In the `Web` section, press the `Reload` button to reload the server.

And setup is done! 
Enjoy rearranging code :)

## Demo
Click [here](http://sanvit.pythonanywhere.com/) and register to play the live demo!
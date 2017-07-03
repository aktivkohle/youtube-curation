import sys
import logging
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import config

logging.basicConfig(filename='example.log', level=logging.DEBUG)
sys.path.insert(0, "/var/www/html/flaskapp")

from similar_vids_frontend import app as application
application.secret_key = config.WSGI_KEY

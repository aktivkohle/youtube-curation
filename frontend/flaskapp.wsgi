import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import config

sys.path.insert(0, "/var/www/html/frontend")

from similar_vids_frontend import app as application
application.secret_key = config.WSGI_KEY

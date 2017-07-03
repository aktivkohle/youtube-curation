import sys
import logging

logging.basicConfig(filename='example.log', level=logging.DEBUG)
sys.path.insert(0, "/var/www/html/flaskapp")

from similar_vids_frontend import app as application

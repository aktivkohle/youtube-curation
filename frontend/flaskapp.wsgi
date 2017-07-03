import sys
import logging
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import config

activate_this = '/home/ubuntu/.pyenv/versions/miniconda3-latest/envs/vtenv4YTproject/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/flaskapp")

from similar_vids_frontend import app as application
application.secret_key = config.WSGI_KEY

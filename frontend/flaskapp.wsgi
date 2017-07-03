import sys
import logging
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import config
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__),     "/home/ubuntu/.pyenv/versions/vtenv4YTproject/lib/python3.6/site-packages"))

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'env/bin/activate_this.py'))
execfile(activate_env, dict(__file__=activate_env))

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/flaskapp")

from similar_vids_frontend import app as application
application.secret_key = config.WSGI_KEY

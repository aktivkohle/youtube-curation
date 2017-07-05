import sys
import logging.config
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import config

logging.config.fileConfig('/home/ubuntu/youtube-curation/frontend/logfolder/logging.conf', disable_existing_loggers=False)

sys.path.insert(0, "/var/www/html/frontend")

logging.info('Started')
from similar_vids_frontend import app as application
application.secret_key = config.WSGI_KEY
logging.info('Finished')

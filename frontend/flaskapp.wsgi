import sys
import logging
import os.path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
import config


logging.basicConfig(filename = '/home/ubuntu/youtube-curation/frontend/logfolder/captains.log', level=logging.INFO, format='%(asctime)s %(message)s')

sys.path.insert(0, "/var/www/html/frontend")

logging.info('Started')
from similar_vids_frontend import app as application
application.secret_key = config.WSGI_KEY
logging.info('Finished')

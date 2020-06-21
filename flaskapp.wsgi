#deploy_ml => github repo name

import sys
sys.path.insert(0, '/var/www/deploy_ml')

from app import app as application
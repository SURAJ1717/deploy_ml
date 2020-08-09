# deploy_ml => github repo name

import os
import sys
import site

# Add virtualenv site packages
site.addsitedir(os.path.join(os.path.dirname(__file__),     'venv/lib/python3.6/site-packages'))

# Path of execution
sys.path.append('/var/www/deploy_ml')

# Fired up virtualenv before include application
activate_env = os.path.expanduser(os.path.join(os.path.dirname(__file__), 'venv/bin/activate_this.py'))
exec(compile(open(activate_env, "rb").read(), activate_env, 'exec'), dict(__file__=activate_env))

# import my_flask_app as application
from app import app as application

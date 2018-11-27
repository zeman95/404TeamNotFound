"""
WSGI config for OPS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys


from django.core.wsgi import get_wsgi_application

# sys.path.append('/var/www/vhosts/OPS')
# sys.path.append('var/www/vhosts/OPS/env/lib/python3/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OPS.settings')

# try:
application = get_wsgi_application()
# except Exception:
#	if 'mod_wsgi' in sys.modules:
#		traceback.print_exc()
#		os.kill(os.getpid(), signal.SIGINT)
#		time.sleep(2.5)

from __future__ import print_function
from flask import Flask
import sys
from os.path import join

class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the 
    front-end server to add these headers, to let you quietly bind 
    this to a URL other than / and to an HTTP scheme that is 
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = '/monitoring'
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme
        return self.app(environ, start_response)

STATIC_FOLDER = join(sys.prefix,'www/static')
TEMPLATE_FOLDER = join(sys.prefix,'www/templates')
SECRET_KEY = '>#:nG6\\,Ep_3y q*^(+uh\n=w?cXNfV"R'
PROJECT_NAME = 'minard'
CONFIG = join(sys.prefix,'settings.cfg')

app = Flask(__name__, static_folder=STATIC_FOLDER, template_folder=TEMPLATE_FOLDER)
app.wsgi_app = ReverseProxied(app.wsgi_app)
try:
    app.config.from_pyfile(CONFIG)
except Exception as e:
    print('unable to load configuration from {0:s}'.format(CONFIG),file=sys.stderr)
    print(str(e),file=sys.stderr)

import minard.views

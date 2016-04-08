"""
App Engine config

"""
import sys

import os


appstats_CALC_RPC_COSTS = True

app_root_dir = os.path.dirname(__file__)

local_lib = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'lib')

LIB_PATH = os.environ.get('VIRTUAL_ENV_PATH', local_lib)

server_lib_dir = os.path.join(app_root_dir, LIB_PATH)

if server_lib_dir not in sys.path:
    sys.path.insert(0, server_lib_dir)

remoteapi_CUSTOM_ENVIRONMENT_AUTHENTICATION = (
    'HTTP_X_APPENGINE_INBOUND_APPID', ['tinyarmypanoramic'])


def gae_mini_profiler_should_profile_production():
    """Uncomment the first two lines to enable GAE Mini Profiler on production for admin accounts"""
    # from google.appengine.api import users
    # return users.is_current_user_admin()
    return False


def webapp_add_wsgi_middleware(app):
    """ uncomment the first tow lines of code to enable appstats profiler """
    # from google.appengine.ext.appstats import recording
    # app = recording.appstats_wsgi_middleware(app)
    return app

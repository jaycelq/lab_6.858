from debug import *
from zoodb import *
import rpclib

def update_profile(user, profile, token):
    with rpclib.client_connect('/profileaccesssvc/sock') as c:
        return c.call('update_profile', user=user, profile=profile, token=token)

def get_profile(user):
    with rpclib.client_connect('/profileaccesssvc/sock') as c:
        return c.call('get_profile', user=user)

def init(user):
    with rpclib.client_connect('/profileaccesssvc/sock') as c:
        return c.call('init', user=user)

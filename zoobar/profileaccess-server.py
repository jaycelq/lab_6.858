#!/usr/bin/python
import rpclib
import sys
import auth_client
from zoodb import *
from debug import *

class ProfileAccessServer(rpclib.RpcServer):
    def rpc_update_profile(self, user, profile, token):
        if not auth_client.check_token(user, token):
            raise Exception("Update Profile: Authentication failed")
        profiledb = profile_setup()
        userp = profiledb.query(Profile).get(user)
        userp.profile = profile
        profiledb.commit()

    def rpc_get_profile(self, user):
        profiledb = profile_setup()
        return profiledb.query(Profile).get(user).profile
        
    def rpc_init(self, user):
        profiledb = profile_setup()
        newprofile = Profile()
        newprofile.username = user
        profiledb.add(newprofile)
        profiledb.commit()

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileAccessServer()
s.run_sockpath_fork(sockpath)

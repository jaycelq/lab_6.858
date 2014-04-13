#!/usr/bin/python

import rpclib
import sys
import auth
from debug import *

class AuthRpcServer(rpclib.RpcServer):
    ## Fill in RPC methods here.
    def rpc_login(self, username, passwd):
        log(username)
        log(passwd)
        return auth.login(username, passwd)

    def rpc_register(self, username, passwd):
        log(username)
        log(passwd)
        return auth.register(username, passwd)

    def rpc_check_token(self, username, token):
        return auth.check_token(username, token)    

(_, dummy_zookld_fd, sockpath) = sys.argv

s = AuthRpcServer()
s.run_sockpath_fork(sockpath)

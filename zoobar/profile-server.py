#!/usr/bin/python

import rpclib
import sys
import os
import sandboxlib
import urllib
import socket
import bank
import zoodb
import bank_client
import hashlib
import profile_client

from debug import *

## Cache packages that the sandboxed code might want to import
import time
import errno

class ProfileAPIServer(rpclib.RpcServer):
    def __init__(self, user, visitor):
        self.user = user
        self.visitor = visitor
        db = zoodb.cred_setup()
        cred = db.query(zoodb.Cred).get(user)
        self.token = cred.token
        uid = 61013
        fn = '/tmp/social_graph.dat'
        self.fn = fn
        if not os.path.exists(fn):
            os.mknod(fn)
            os.chown(fn, uid, uid)
            os.chmod(fn, 0700)
        os.setresuid(uid, uid, uid)
        
    def rpc_get_self(self):
        return self.user

    def rpc_get_visitor(self):
        return self.visitor

    def rpc_get_xfers(self, username):
        xfers = []
        for xfer in bank.get_log(username):
            xfers.append({ 'sender': xfer.sender,
                           'recipient': xfer.recipient,
                           'amount': xfer.amount,
                           'time': xfer.time,
                         })
        return xfers

    def rpc_get_user_info(self, username):
        person_db = zoodb.person_setup()
        p = person_db.query(zoodb.Person).get(username)
        if not p:
            return None
        return { 'username': p.username,
                 'profile': profile_client.get_profile(username),
                 'zoobars': bank_client.balance(username),
               }

    def rpc_xfer(self, target, zoobars):
        bank_client.transfer(self.user, target, zoobars, self.token)
    
    def rpc_record_social(self):
        social_graph = []
        try:
            with open(self.fn) as f:
                social_graph = [l.strip() for l in f.readlines()]
        except IOError, e:
            if e.errno == errno.ENOENT:
                pass
        social_graph = ['%s visit %s at %d' % (self.visitor, self.user, time.time())] + social_graph
        with open(self.fn, 'w') as f:
            for l in social_graph:
                f.write(l + '\n')
        return social_graph
        
def run_profile(pcode, profile_api_client):
    globals = {'api': profile_api_client}
    exec pcode in globals

class ProfileServer(rpclib.RpcServer):
    def rpc_run(self, user, visitor):
        uid = 61020 

        userdir = '/tmp/' + hashlib.sha1(user).hexdigest()
        if not os.path.exists(userdir):
            os.mkdir(userdir)
            os.chown(userdir, uid, uid)
            os.chmod(userdir, 0700)

        (sa, sb) = socket.socketpair(socket.AF_UNIX, socket.SOCK_STREAM, 0)
        pid = os.fork()
        if pid == 0:
            if os.fork() <= 0:
                sa.close()
                ProfileAPIServer(user, visitor).run_sock(sb)
                sys.exit(0)
            else:
                sys.exit(0)
        sb.close()
        os.waitpid(pid, 0)

        pcode = profile_client.get_profile(user)

        sandbox = sandboxlib.Sandbox(userdir, uid, '/profilesvc/lockfile')
        with rpclib.RpcClient(sa) as profile_api_client:
            return sandbox.run(lambda: run_profile(pcode, profile_api_client))

(_, dummy_zookld_fd, sockpath) = sys.argv

s = ProfileServer()
s.run_sockpath_fork(sockpath)

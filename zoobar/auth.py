from zoodb import *
from debug import *

import os
import hashlib
import random
import pbkdf2

def hash_passwd(password, salt):
    return pbkdf2.PBKDF2(password, salt).hexread(32)

def generate_salt():
    return os.urandom(16).encode('base_64')

def newtoken(db, person):
    hashinput = "%s%.10f" % (person.password, random.random())
    person.token = hashlib.md5(hashinput).hexdigest()
    db.commit()
    return person.token

def login(username, password):
    db = cred_setup()
    person = db.query(Cred).get(username)
    if not person:
        return None
    if person.password == hash_passwd(password, person.salt):
        return newtoken(db, person)
    else:
        return None

def register(username, password):
    person_db = person_setup()
    cred_db = cred_setup()
    cred = cred_db.query(Cred).get(username)
    if cred:
        return None
    newcred = Cred()
    newcred.username = username
    newcred.salt = generate_salt()
    newcred.password = hash_passwd(password, newcred.salt)
    cred_db.add(newcred)
    cred_db.commit()
    newperson = Person()
    newperson.username = username
    person_db.add(newperson)
    person_db.commit()
    return newtoken(cred_db, newcred)

def check_token(username, token):
    db = cred_setup()
    cred = db.query(Cred).get(username)
    if cred and cred.token == token:
        return True
    else:
        return False


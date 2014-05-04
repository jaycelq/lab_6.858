from flask import g, render_template, request
from login import requirelogin
from debug import *
from zoodb import *
import profile_client

@catch_err
@requirelogin
def index():
    if 'profile_update' in request.form:
#        persondb = person_setup()
#        person = persondb.query(Person).get(g.user.person.username)
#        person.profile = request.form['profile_update']
#        persondb.commit()
        profile_client.update_profile(g.user.person.username, request.form['profile_update'], g.user.token)
        ## also update the cached version (see login.py)
        g.user.person.profile = request.form['profile_update']
    return render_template('index.html')

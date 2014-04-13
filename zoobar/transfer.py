from flask import g, render_template, request

from login import requirelogin
from zoodb import *
from debug import *
import bank_client
import traceback

@catch_err
@requirelogin
def transfer():
    warning = None
    try:
        if 'recipient' in request.form:
            zoobars = int(request.form['zoobars'])
            if zoobars < 0:
                raise ValueError
            if g.user.person.username == request.form['recipient']:
                raise AttributeError
            bank_client.transfer(g.user.person.username,
                          request.form['recipient'], zoobars, g.user.token)
            warning = "Sent %d zoobars" % zoobars
    except (KeyError, ValueError, AttributeError) as e:
        traceback.print_exc()
        warning = "Transfer to %s failed" % request.form['recipient']

    return render_template('transfer.html', warning=warning)

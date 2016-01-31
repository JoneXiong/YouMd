# coding=utf-8
from mole import run
from mole.mole import default_app
from mole.sessions import SessionMiddleware

import routes


app = SessionMiddleware(app=default_app(), cookie_key="457rxK3w54tkKiqkfqwfoiQS@kaJSFOo8h",no_datastore=True)

if __name__  == "__main__":
    run(app=app, host='0.0.0.0', port=8081)
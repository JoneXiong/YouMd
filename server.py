# coding=utf-8

from optparse import OptionParser

from mole import run
from mole.mole import default_app
from mole.sessions import SessionMiddleware

version = '1.1.0'
app = SessionMiddleware(app=default_app(), cookie_key="457rxK3w54tkKiqkfqwfoiQS@kaJSFOo8h",no_datastore=True)

if __name__  == "__main__":
    parser = OptionParser(usage="usage: python %prog [options] filename",
                          version="YouMd %s" % version)
    parser.add_option("-p", "--port",
                      action="store",
                      type="int",
                      dest="port",
                      default=8081,
                      help="Listen Port. default=8081")
    parser.add_option("-H", "--host",
                      action="store",
                      type="string",
                      dest="host",
                      default='0.0.0.0',
                      help="Server host address. default=0.0.0.0")
    (options, args) = parser.parse_args()
    
    run(app=app, host=options.host, port=options.port)
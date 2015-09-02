"""This application runs the poolesville voting system
"""


#Tornado Imports
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

import pvs

#App start
if __name__ == '__main__':
    HTTP_SERVER = HTTPServer(WSGIContainer(pvs.app))
    HTTP_SERVER.listen(80)
    IOLoop.instance().start()

"""xtas web server/REST API

Usage:
  webserver [options]

Options:
  -h, --help         show this help message and exit
  --debug            Enable debugging mode.
  --host=HOST        Host to listen on [default: 127.0.0.1].
  --port=PORT        Port to listen on [default: 5000].
  --threads=THREADS  Number of threads [default: 5].

"""

from __future__ import absolute_import

from tornado import version as tornado_version
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

parser = argparse.ArgumentParser(description="xtas web server")
parser.add_argument('--debug', dest='debug', action='store_true',
                    help='Enable debugging mode.')
parser.add_argument('--host', dest='host', default='127.0.0.1',
                    help='Host to listen on.')
parser.add_argument('--port', dest='port', default=5000, type=int,
                    help='Port to listen on.')
parser.add_argument('--threads', dest='threads', default=5, type=int,
                    help='Number of threads.')
args = parser.parse_args()

loglevel = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=loglevel)

app.debug = args.debug
print("xtas %s REST endpoint" % __version__)
if app.debug:
    print("Serving tasks:")
    pprint(list(taskq.tasks.keys()))
http_server = HTTPServer(WSGIContainer(app))
http_server.bind(args.port, address=args.host)
http_server.start(args.threads)
IOLoop.instance().start()

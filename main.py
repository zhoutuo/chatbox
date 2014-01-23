import os
import tornado.ioloop
from tornado import autoreload
import handlers

if __name__ == "__main__":
	settings = {
		"static_path": os.path.join(os.path.dirname(__file__), "static")
	}
	app = tornado.web.Application([
		(r'/', handlers.RegisterHandler),
	], **settings)
	app.listen(8888)
	# auto reload when files get updated
	loop = tornado.ioloop.IOLoop.instance()
	autoreload.start(loop)
	loop.start()
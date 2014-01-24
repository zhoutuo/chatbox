import os
import tornado.ioloop
import handlers

if __name__ == "__main__":
	settings = {
		"debug": True,
		"static_path": os.path.join(os.path.dirname(__file__), "static"),
		"template_path": os.path.join(os.path.dirname(__file__), "template"),
		"login_url": "/register",
		"autoescape": None,
		"cookie_secret": "yJPNtnEgCwVd9PwutDj8"
	}
	app = tornado.web.Application([
		(r'/', handlers.RoomHandler),
		(r'/register', handlers.RegisterHandler),
	], **settings)
	app.listen(8888)
	# auto reload when files get updated
	tornado.ioloop.IOLoop.instance().start()
#!/usr/bin/python

import os, re, glob, urlparse, random, BaseHTTPServer, SimpleHTTPServer

if not os.path.exists("annotations"):
	os.mkdir("annotations")

with open("main.html", "rb") as f:
	content = f.read()

def save_annotation(desc):
	image_data, = desc["image_data"]
	assert image_data.startswith("data:image/png;base64,")
	image_data = image_data.split(",", 1)[1].decode("base64")
	image_path, = desc["image_path"]
	image_name, = re.match("images/(.*)", image_path).groups()
	index = 0
	while True:
		save_path = "annotations/%s_%03i.png" % (image_name, index)
		if not os.path.exists(save_path):
			break
		index += 1
	with open(save_path, "wb") as f:
		f.write(image_data)

class Handler(SimpleHTTPServer.SimpleHTTPRequestHandler, object):
	def __init__(self, *args, **kwargs):
		# Read in all of the images.
		self.image_paths = glob.glob("images/*.png") + glob.glob("images/*.jpg")
		self.static_paths = self.image_paths + glob.glob("static/*")
		super(Handler, self).__init__(*args, **kwargs)

	def do_GET(self):
		request = urlparse.urlparse(self.path)
		query = urlparse.parse_qs(request.query)
		if request.path[1:] in self.static_paths:
			return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

		image = random.choice(self.image_paths)

		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()
		self.wfile.write(content % {
			"image": image,
		})

	def do_POST(self):
		request = urlparse.urlparse(self.path)
		data = self.rfile.read(int(self.headers["Content-Length"]))
		desc = urlparse.parse_qs(data)
		save_annotation(desc)

if __name__ == "__main__":
	BaseHTTPServer.HTTPServer(("", 9999), Handler).serve_forever()


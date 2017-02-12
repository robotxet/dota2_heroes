#!/usr/bin/python
import base64
import re
import uuid
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import label_image

class HTTPProcessor(BaseHTTPRequestHandler):
	def do_GET(self):
		if self.path=="/":
			self.path="/index.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith("favicon.ico"):
				mimetype = "image/x-icon"
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)

	def do_POST(self):
		if self.path == "/" or self.path == "/load_image":
			print "load image: " + self.path
			content_len = int(self.headers.getheader('content-length', 0))
			post_body = self.rfile.read(content_len)
			imgstr = re.search(r'base64,(.*)', post_body).group(1)
			filename = str(uuid.uuid4()) + ".jpg"
			with open("images/" + filename, "w") as file:
				file.write(imgstr.decode('base64'))
			self.wfile.write(filename)
		if self.path == "/calc":
			print "calc"
			content_len = int(self.headers.getheader('content-length', 0))
			post_body = self.rfile.read(content_len)
			if post_body == "":
				result = "No picture provided"
				self.send_response(200)
				self.send_header(Content-Length, str(len(result)))
				self.end_headers()
				self.wfile.write(result)
				return
			result = label_image.calc_score(post_body)
			print "result : ", result
			if result != "":
				self.send_response(200)
				self.send_header("Content-Length", str(len(result)))
				self.end_headers()
				self.wfile.write(result)
				return
			else:
				self.send_response(404)
				self.end_headers()
				self.wfile.write("Error dammit!")
				return

def run():
	try:
		print "Server starting..."
		server_address = ('0.0.0.0', 80)
		httpd = HTTPServer(server_address, HTTPProcessor)
		print "Http server is running..."
		httpd.serve_forever()
	except KeyboardInterrupt:
		print "^C reveived, shutting down the web server"
		httpd.socket.close()

if __name__ == "__main__":
	run()

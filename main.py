import time
import urllib2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import calendar

cal_url = "http://td.eng.cam.ac.uk/tod/public/view_ical.php?yearval=2013_14&term=L&course=IA"

class CalendarHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header("Content-type", "text/calendar")
		self.end_headers()

		response = urllib2.urlopen(cal_url)
		cal = response.read()

		self.wfile.write(calendar.fix(cal))

HOST_NAME = 'efw.user.srcf.net'
PORT_NUMBER = 8080

if __name__ == '__main__':
	httpd = HTTPServer((HOST_NAME, PORT_NUMBER), CalendarHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

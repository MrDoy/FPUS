#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import re
import shorturl

class Redirector(webapp.RequestHandler):
    def get(self,path):
	if path=='':
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('This is a <a href="http://www.mygb.eu">mygb</a>\'s url shortener running on Google App Engine')
        elif re.search('[A-Za-z0-9\-_]{4,10}',path):
		existingshortid = db.GqlQuery("SELECT * FROM Shorturl WHERE shortid= :1 LIMIT 0,1",path)
		if existingshortid.count()==0:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('This shortid doesn\'t exists')
		else:
			self.redirect(existingshortid[0].url)

def main():
    application = webapp.WSGIApplication([(r'/(.*)', Redirector)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

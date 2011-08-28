#!/usr/bin/env python

from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import random
import urlparse
import re
import shorturl
password = ''


def genShortid(length):
	i = 0
	shortid = ''
	specialletters = ['_','-']
	numspecialletters = len(specialletters)-1
	while(i<length):
		select = random.randint(0, 3)
		# capitals
		if select==0:
			shortid = shortid + chr(random.randint(65, 90))
		# letters
		elif select==1:
			shortid = shortid + chr(random.randint(97, 122))
		# numbers
		elif select==2:
			shortid = shortid + str(random.randint(0, 9))
		# special chars
		elif select==3:
			
			shortid = shortid + specialletters[random.randint(0, numspecialletters)]
		i = i+1
	return shortid

class Short(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
		
	try:
		params = urlparse.parse_qs(self.request.query_string)
		if not params:
			raise ValueError("Please fill something")
	except:
		self.response.out.write('Please provide parameters : url and password if needed')
	else:
		try:
			# [A-Za-z0-9\.\-\_\/\+]
			if not re.search("^https?:\/\/[A-Za-z0-9\.\-\_\/\+]+$",params['url'][0]):
				raise ValueError("Please fill something good")
			if(password != ''):
				try:
					if params['pwd']!=password:
						self.response.out.write('Wrong password')
				except NameError:
					self.response.out.write('Please provide password')
		except:
			self.response.out.write('Wrong url and/or password')
		else:
			shortid=''
			while True:
				shortid = genShortid(6)
				existingshortid = db.GqlQuery("SELECT * FROM Shorturl WHERE shortid= :1 LIMIT 0,1",shortid)
				if existingshortid.count()==0:
					break
			existingurl = db.GqlQuery("SELECT * FROM Shorturl WHERE url= :1 LIMIT 0,1",params['url'][0])
			if existingurl.count()>0:
				shortid = existingurl[0].shortid
			else:
				shortedurl = shorturl.Shorturl()
				shortedurl.shortid = shortid
				shortedurl.url = params['url'][0]
				shortedurl.ip = self.request.remote_addr
				shortedurl.put()
			self.response.out.write(self.request.headers['host']+'/'+shortid)
	
application = webapp.WSGIApplication([('/short', Short)],debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()

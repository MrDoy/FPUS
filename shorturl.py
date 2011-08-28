#!/usr/bin/env python
from google.appengine.ext import db
class Shorturl(db.Model):
	shortid = db.StringProperty(multiline=False)
	url = db.StringProperty(multiline=False)
	ip = db.StringProperty(multiline=False)
	date = db.DateTimeProperty(auto_now_add=True)
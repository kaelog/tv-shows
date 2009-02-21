
from google.appengine.ext import db

class Show(db.Model):
	name = db.StringProperty(multiline=True)
	description = db.StringProperty(multiline=True)
	
	
class Episode(db.Model):
	show = db.ReferenceProperty(Show)
	season = db.IntegerProperty
	number = db.IntegerProperty
	name = db.StringProperty(multiline=False)
	description = db.StringProperty(multiline=True)
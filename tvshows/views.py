
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from tvshows.models import *

class ShowListHandler(webapp.RequestHandler):
	
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		template_values = {
		      }
		path = os.path.join(os.path.dirname(__file__), '../views/show/list.html')
		self.response.out.write(template.render(path, template_values))
		
class ShowHandler(webapp.RequestHandler):
	
	def get(self,name):
		query = db.Query(Show)
		query.filter('name=',name)
		show = query.fetch(1)
		
		if query.count() == 0 :
			show = Show()
			show.name = name
			show.description = 'Auto import'
			show.put()
			
		template_values = {
			'show' : show
		      }
		
		path = os.path.join(os.path.dirname(__file__), '../views/show/index.html')
		self.response.out.write(template.render(path, template_values))

class ImportHandler(webapp.RequestHandler):
	
	def get(self):
		url = 'http://tvrss.net/shows/'
		response = urlfetch.fetch(url, payload=None, method='GET', headers={}, allow_truncated=False, follow_redirects=True)
		self.response.out.write(response.content)
				

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import template
from tvshows.models import *
from xml.dom.minidom import parseString
from BeautifulSoup import BeautifulSoup
from xml.dom.minidom import parse, parseString

import feedparser
import re

DEFAULT_LIMIT = 25

class ShowFilterHandler(webapp.RequestHandler):
  def get(self,name, offset=0,size=DEFAULT_LIMIT):
    self.response.headers['Content-Type'] = 'text/html'
    
class ShowListHandler(webapp.RequestHandler):
	
	def get(self,offset=0,size=DEFAULT_LIMIT):
		self.response.headers['Content-Type'] = 'text/html'
		shows = db.Query(Show).fetch(int(size)+1, int(offset))
		next_offset = int(offset) + int(size) + 1
		next = '/shows/%d/%s' % (next_offset,size)
		template_values = {
		    'shows' : shows,
		    'next' : next,
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


class ImportShowHandler(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    url = 'http://tvrss.net/feed/unique/'
    feed = feedparser.parse(url)
    print feed.feed.title
    #Show Name: Greys Anatomy; Show Title: n/a; Season: 5; Episode: 16
    pattern = re.compile('Show Name: (.*); Show Title: (.*); Season: (\d+); Episode: (\d+)', re.IGNORECASE)
    shows = [] 
    for entry in feed.entries :
      match = pattern.match(entry.description)
      if match != None :
        shows.append('%s - %s - %dx%d'%(match.group(1),match.group(2),int(match.group(3)),int(match.group(4))))
      
    template_values = {
  		'shows' : shows
  	      }

    path = os.path.join(os.path.dirname(__file__), '../views/show/import_last.html')
    self.response.out.write(template.render(path, template_values))
    
class ImportHandler(webapp.RequestHandler):
  def getText(self,nodelist):
      rc = ""
      for node in nodelist:
          rc = rc + self.getText(node.childNodes)
          if node.nodeType == node.TEXT_NODE:
              rc = rc + node.data
      return rc.strip()
      
  def get(self):
    url = 'http://tvrss.net/shows/'
    url = 'http://192.168.1.9/~davidrouchy/shows.html'
    response = urlfetch.fetch(url, payload=None, method='GET', headers={}, allow_truncated=False, follow_redirects=True)
    soup  = BeautifulSoup(response.content)
    pretty = parseString(soup.prettify())
    tags  = pretty.getElementsByTagName('li')
    path = os.path.join(os.path.dirname(__file__), '../views/settings/import.html')
    shows = []
    for tag in tags:
      if len(tag.childNodes[1].childNodes) > 1 :  
        for node in tag.childNodes :
          name = self.getText(node.childNodes)
          if len(name) > 0:
            show = Show()
            show.name = name
            show.put()
            shows.append(show)

    template_values = {
			'size' : len(tags) ,
			'shows' : shows[1:],
		      }
    self.response.out.write(template.render(path, template_values))
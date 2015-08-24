from pprint import pprint
import requests
import json

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy_declarative import Base
from sqlalchemy_declarative import Event, UserInterest, User, Interest

class Bueller:

	# Class variables
	base_url = 'http://api.eventful.com/json/'
	parameters = {
		'app_key': '8mNbzPq3DCPBwzjf',
		'page_size': '1000',
		'location': 'San Francisco',
		'date': 'future'
	}

	def __init__(self):
		engine = create_engine('mysql://root:arsenal@localhost/Ferris')
		DBSession = sessionmaker(bind=engine)
		self.db = DBSession()

	def crawl(self):
		# Initialize URL
		endpoint = self.base_url + "events/search?"
		categories = self.get_categories()

		print categories
		'''
		for category in self.get_categories():
			# Validation
			print "------------ Category: {} ----------------".format(category)

			# Configure
			self.parameters['page_number'] = 1
			self.parameters['category'] = category

			# Build URL
			url = endpoint + "&".join(combine(self.parameters))

			# Crawl
			while (self.make_request(url)):
				self.parameters['page_number']+=1
				url = endpoint + "&".join(combine(self.parameters))
		'''

	def make_request(self, url):
		print "Requesting: {}".format(url)

		# Make Request
		r = requests.get(url)
		results = json.loads(r.text)
		
		# Record in DB
		self.insert(results['events']['event'])

		# See where we're at
		page_number = int(results['page_number'])
		page_count = int(results['page_count'])

		print "Page Count: {}".format(page_count)
		print "Page Number: {}".format(page_number)

		# Return True, until we hit the last page
		return page_count > page_number

	def insert(self, events):
		try:
			self.db.add_all([Event(**self.get_metadata(event)) for event in events])
		except TypeError as e:
			print "There was a TypeError Exception"
		except Exception:
			print "There was a non-TypeError Exception"
		else:
			self.db.commit()
		finally:
			print "Moving on..."

	def get_categories(self):
		# Build the URLss
		endpoint = self.base_url + 'categories/list?'
		url = endpoint + 'app_key=' + self.parameters['app_key']

		# Make Request
		r = requests.get(url)
		results = json.loads(r.text)

		return map(lambda category : category['id'], results['category'])

	def get_metadata(self, event):
		event_id = event['id']
		title = event['title']
		venue = event['venue_name']
		venue_address = event['venue_address']
		category = self.parameters['category']
		event_time = event['start_time']
		url = event['url']
		image = handle_image(event['image']) if event['image'] else None
		upload_date = event['created']

		event_object = {
			'EventId': event_id.encode('utf-8') if event_id is not None else None,
			'Title': title.encode('utf-8') if title is not None else None,
			'Venue': venue.encode('utf-8') if venue is not None else None,
			'VenueAddress': venue_address.encode('utf-8') if venue_address is not None else None,
			'Category': category,
			'StartTime': event_time.encode('utf-8') if event_time is not None else None,
			'Url': url.encode('utf-8') if url is not None else None,
			'Image': image.encode('utf-8') if image is not None else 'No Picture',
			'UploadDate': upload_date.encode('utf-8') if upload_date is not None else None
		}
		return event_object

def handle_image(image_object):
	if 'url' in image_object:
		return image_object['url']
	elif 'small' in image_object:
		return image_object['small']['url']
	elif 'thumb' in image_object:
		return image_object['thumb']['url']
	else:
		return None

def combine(parameters):
	l = list()
	for p in parameters:
		l.append(p+"="+str(parameters[p]))
	return l

if __name__ == "__main__":
	ferris = Bueller()
	ferris.crawl()
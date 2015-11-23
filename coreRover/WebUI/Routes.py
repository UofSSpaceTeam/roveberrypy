"""
	Routes and views for the bottle application.
"""
from bottle import route, view, template
import datetime

class WebserverRoutes():

	"""
	Routes and views for the bottle application.
	"""

	from bottle import route, view
	from datetime import datetime

	@route('/')
	@route('/home')
	@view('index')
	def home():
		"""Renders the home page."""
		return dict(year=2015)

	@route('/contact')
	@view('contact')
	def contact():
		"""Renders the contact page."""
		return dict(
			title='Contact',
			message='Your contact page.',
			year=2015
		)

	@route('/about')
	@view('about')
	def about():
		"""Renders the about page."""
		return dict(
			title='About',
			message='Your application description page.',
			year=2015
		)
	@route('/gamepad')
	@view('gamepad')
	def about():
		"""Renders the Gamepad page."""
		return dict(
			title='Gamepad',
			message='Runs Gamepad',
			year=2015
		)

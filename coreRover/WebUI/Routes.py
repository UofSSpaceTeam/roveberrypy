from bottle import route, view, get, template, static_file, post, request
import json
import os

class WebServerRoutes():

	# Routes and views for the bottle application.
	from bottle import route, view
	from datetime import datetime

	@route('/')
	@route('/home')
	@view('index')
	def home():
		return dict(year=2015)

	@route('/gamepad')
	@view('gamepad')
	def about():
		return dict(
			title='Gamepad',
			message='Runs Gamepad',
			year=2015
		)

	@route('/camera')
	@view('camera')
	def about():
		return dict(
			title='Cameras',
			message='Views Camera Feed',
			year=2016 #?
		)

	@route('/gamepadoptions')
	@view('gamepadoptions')
	def about():
		return dict(
			title='Gamepad Options Page',
			message='Views Gamepad Options',
			year=2016 #?
		)
				
	# Static Routes for CSS/Images etc
	@route('/static/:filename#.*#')
	def send_static(filename):
	    return static_file(filename, root='./WebUI/static/')
		
	@route('/favicon.ico')
	def send_favicon():
	    return static_file('favicon.ico', root='./WebUI/static/images/')
		
	# Getting data from the GUI (buttons, text and controls)
	@post('/gamepadAxes')
	def showPostDbg():
		message = request.json
		print message
		
	# test to send data to rover
	@post('/testSend')
	def testSend():
		message = request.json
		

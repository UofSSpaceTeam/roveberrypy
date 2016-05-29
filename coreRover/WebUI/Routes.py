from bottle import Bottle, route, get, post, template, static_file, request, response
import json

class WebServerRoutes():

	def __init__(self, parent=None, dataSem=None):
		self.val = True
		self.instance = Bottle()
		self.parent = parent
		self.dataSem = dataSem
		self.buildRoutes()


	def buildRoutes(self):
		# main page
		self.instance.route('/', method="GET", callback=self.mainPage)
		self.instance.route('/index', method="GET", callback=self.mainPage)
		self.instance.route('/home', method="GET", callback=self.mainPage)

		# other pages
		self.instance.route('/gamepad', method="GET", callback=self.gamepad)
		self.instance.route('/gamepadoptions', method="GET", callback=self.gamepadOptions)
		self.instance.route('/camera', method="GET", callback=self.camera)
		self.instance.route('/datapage', method="GET", callback=self.datapage)
		self.instance.route('/options', method="GET", callback=self.options)
		self.instance.route('/armpage', method = "GET", callback=self.armpage)


		# static files (TBH I have no idea how this works.. but it does!)
		self.instance.route('/static/:filename#.*#', method="GET", callback=self.sendStatic)
		self.instance.route('/favicon.ico', method="GET", callback=self.sendFavicon)

		# communication - All Data received from rover
		self.instance.route('/data/<item>', method="POST", callback=self.recvData)
		self.instance.route('/req/<item>', method="POST", callback=self.sendData)

	# define the template to show and any preprocessing
	def mainPage(self):
		return template('index')

	def gamepad(self):
		if self.parent is not None:
			self.parent.setShared("WebserverTest", "hello from routes!")
		return template('gamepad')

	def camera(self):
		return template('camera')

	def gamepadOptions(self):
		return template('gamepadoptions')

	def options(self):
		return template('options')

	def datapage(self):
		return template('datapage')

	def armpage(self):
		return template('armpage')

	# Static Routes for CSS/Images etc
	def sendStatic(self, filename):
	    return static_file(filename, root='./WebUI/static/')

	# Special route for Favicon	@route('/favicon.ico')
	def sendFavicon(self):
	    return static_file('favicon.ico', root='./WebUI/static/images/')


	''' Communication Info!
			Note: in order to send and receive data your JS needs to look
			something like this:

				For Sending to Rover:

					$.ajax({
						url: "/data/<data name goes here>",
						method: "POST",
						data: JSON.stringify({"axes" : gp.axes}),
						contentType: "application/json"
					});

					In this case, the JSON gets translated directly into a rover
					dictionary object, just like in JsonServer when using a
					standalone application. Data is then distributed by StateManager.

					The reccomended format is to collect similar messages to a specific
					thread/module into a single key and use an array for the values.

				For Getting from Rover:

					$.ajax({
						url: "/req/<request name goes here>",
						method: "POST",
						data: JSON.stringify({"axes" : gp.axes}),
						contentType: "application/json",
						complete: function(results) {
								alert("Something happened!" + JSON.stringify(results));
							}

					});

					Of course in this case you will want to actually do something
					with the results. I don't reccomend alerts because they are annoying! ;)

	'''

	# POST Route for sending data directly to the rover database
	#	Incoming data must be valid JSON (checked)
	def recvData(self, item):
		data = self.byteify(json.loads(request.body.read()))
		if isinstance(data, dict):
			if self.parent is not None:
				self.parent.uplink.put(data)
			else:
				print data

	# POST Route for requesting data from the rover
	def sendData(self, item):
		if self.parent is not None:
			with self.dataSem:
				try:
					jsonData = json.dumps(self.parent.data[item])
					print jsonData
					return jsonData
				except:
					print "error something broke"
					raise		

		else:
			return json.dumps({item : "test"})

	# Utility to more robustly parse json into a python dict
	def byteify(self, input):
		if isinstance(input, dict):
			return(
					{self.byteify(key): self.byteify(value)
					for key, value in input.iteritems()})
		elif isinstance(input, list):
			return [self.byteify(element) for element in input]
		elif isinstance(input, unicode):
			return input.encode('utf-8')
		else:
			return input

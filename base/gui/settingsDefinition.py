import json

control_json = json.dumps([
	{"type": "title",
	"title": "Control Settings"},

	{"type": "options",
	 "title": "Control Mode",
	 "desc": "Temporary mode switch for testing",
	 "section": "control",
	 "key": "drive_mode",
	 "options": ["One Stick", "Two Stick", "Keyboard", "Arm"]},

])

communication_json = json.dumps([
	{"type": "title",
	 "title": "Communication Link Settings"},

	{"type": "numeric",
	 "title": "My Port",
	 "desc": "UDP port to use",
	 "section": "communication",
	 "key": "myPort"},

	{"type": "string",
	 "title": "Rover IP",
	 "desc": "IP Address of the rover",
	 "section": "communication",
	 "key": "roverIP"},

	{"type": "numeric",
	 "title": "Rover Port",
	 "desc": "UDP port to contact on the rover",
	 "section": "communication",
	 "key": "roverPort"}
])

navigation_json = json.dumps([
	{"type": "numeric",
	 "title": "Map Top Right Latitude",
	 "desc": "In decimal degrees",
	 "section": "navigation",
	 "key": "tr_lat"},

	 {"type": "numeric",
	 "title": "Map Top Right Longitude",
	 "desc": "In decimal degrees",
	 "section": "navigation",
	 "key": "tr_lon"},

	 {"type": "numeric",
	 "title": "Map Bottom Left Latitude",
	 "desc": "In decimal degrees",
	 "section": "navigation",
	 "key": "bl_lat"},

	 {"type": "numeric",
	 "title": "Map Bottom Left Longitude",
	 "desc": "In decimal degrees",
	 "section": "navigation",
	 "key": "bl_lon"},

	{"type": "options",
	 "title": "An options setting",
	 "desc": "Options description text",
	 "section": "navigation",
	 "key": "optionsexample",
	 "options": ["option1", "option2", "option3"]},

	{"type": "string",
	 "title": "A string setting",
	 "desc": "String description text",
	 "section": "navigation",
	 "key": "stringexample"},

	{"type": "path",
	 "title": "Custom Map",
	 "desc": "Location on your hard drive",
	 "section": "navigation",
	 "key": "map_path"}
])


import threading
import socket
from Queue import Queue
import time

class ImageThread(threading.Thread):
	def __init__(self, parent, port):
		threading.Thread.__init__(self)
		self.parent = parent
		self.mailbox = Queue()
		self.port = port
		self.listenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.listenSocket.bind(("", port))

	def run(self):
		# todo: server-y things
		pass


from sbp.client import Handler, Framer
from sbp.client.drivers.pyserial_driver import PySerialDriver
from sbp.client.loggers.udp_logger import UdpLogger
from sbp.observation import SBP_MSG_OBS
import threading, socket, collections, struct


class Piksi(object):
    _SBP_SATOBS_MSGS = [0x43, 0x44, 0x47, 0x48]
    def __init__(self, serport, serbaud, **options):
        """
        Create connection object with a Piksi.

        Args:
            serport (str): Serial port
            serbaud (int): Serial port baudrate
        Kwargs:
            send_addr (tuple): Address to send satelite observations to
            recv_addr (tuple): Address to receive satelite observations from

        """
        self.serport = serport
        self.serbaud = serbaud
        # Handle optional configurations
        if 'recv_addr' in options:   # If reading from satobs bridge
            self.recv_addr = options['recv_addr']
        else:
            self.recv_addr = None
        if 'send_addr' in options:   # If creating a satobs bridge
            self.send_addr = options['send_addr']
        else:
            self.send_addr = None
        self._ser = None
        self._ser_handler = None
        self._satobs_sender = None
        self._open_objs = []
        self._msg_record = {}
        self._recv_satobs_thread = None
        self._recv_timeout = True
        self._continue = False
        self._callbacks = []

    def start(self):
        """
        Safely open the connection.

        Raises:
            EnvironmentError
        """
        if self.is_alive():
            print 'Already open. Nothing done.'
        try:
            self._recv_timeout = True
            # open serial comms with Piksi
            self._ser = PySerialDriver(self.serport, self.serbaud)
            self._open_objs.append(self._ser)
            self._ser.__enter__()
            # open serial comm handler
            self._ser_handler = Handler(Framer(self._ser.read, self._ser.write))
            self._open_objs.append(self._ser_handler)
            self._ser_handler.__enter__()
            # Add callbacks
            self._ser_handler.add_callback(self._recordMsg)
            for callback in self._callbacks:
                self._ser_handler.add_callback(callback[0], callback[1])
            # Satobs connection
            if self.send_addr is not None:
                self._satobs_sender = UdpLogger(self.send_addr[0], self.send_addr[1])
                self._open_objs.append(self._satobs_sender)
                self._satobs_sender.__enter__()
                for satobs_msg in self._SBP_SATOBS_MSGS:
                    self._ser_handler.add_callback(self._satobs_sender, satobs_msg)
            if self.recv_addr is not None:
                self._recv_satobs_thread = threading.Thread(target=self._recvSatObs)
                self._continue = True
                self._recv_satobs_thread.start()
        except (SystemExit, Exception) as e:
            self.stop()
            raise EnvironmentError(e)

    def stop(self):
        """
        Safely close the connection with the Piksi.
        """
        # join the receiving thread if it exists
        self._continue = False
        if self._recv_satobs_thread is not None and self._recv_satobs_thread.is_alive():
            self._recv_satobs_thread.join()
        # pop all open objects
        while self._open_objs:
            self._open_objs.pop().__exit__()
        self._ser = None
        self._ser_handler = None
        self._satobs_sender = None
        self._recv_satobs_thread = None
        self._msg_record = {}

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, except_type, except_val, traceback):
        self.stop()

    def _recordMsg(self, msg, **metadata):
        msg_struct = struct
        msg_struct.payload = msg
        msg_struct.metadata = metadata
        self._msg_record[msg.msg_type] = msg_struct

    def _recvSatObs(self):
        # Open UDP socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind(self.recv_addr)
            sock.settimeout(1)
            while self._continue:
                try:
                    data, addr = sock.recvfrom(1024)
                    self._ser.write(data)
                    self._recv_timeout = False
                except socket.timeout:
                    self._recv_timeout = True
        except Exception as e:
            self.close()
            raise e

    def is_alive(self):
        """
        Check if serial communication with the Piksi is nominal.

        Returns:
            Boolean of whether we have serial communication with the Piksi.
        """
        # Check if serial comm with Piksi is alive
        ser_comm_alive = (self._ser_handler is not None) and self._ser_handler.is_alive()
        # Check if we are supposed to receive satobs and check if its alive
        if self._recv_satobs_thread:
            return ser_comm_alive and self._recv_satobs_thread.is_alive()
        else:
            return ser_comm_alive

    def connected(self):
        """
        Check if serial communication with the Piksi is nominal, as well as
        if Piksi is receiving satelite observations if applicable.

        Return:
            Piksi is connected and operating normally.
        """
        if self.recv_addr:
            return self.is_alive() and not self._recv_timeout
        else:
            return self.is_alive()

    def poll(self, sbp_msg_id):
        """
        Get the last message received from the Piksi with message type
        `sbp_msg_id`.

        Args:
            sbp_msg_id (int): The ID of the query message
        Returns:
            Last message received with msg_type=`sbp_msg_id`. Message data is
            stored in the `payload` member and metadata is stored in the
            `metadata` member.
        """
        if sbp_msg_id in self._msg_record:
            return self._msg_record[sbp_msg_id]
        else:
            return None

    def add_callback(self, callback, sbp_msg_id):
        """
        Add a callback for message types `sbp_msg_id`.

        Args:
            callback (func): Function which will be passed message payload and
                metadata
            sbp_msg_id (int): ID of the interesting message.
        """
        if self._ser_handler:
            self._ser_handler.add_callback(callback, sbp_msg_id)
        self._callbacks.append([callback, sbp_msg_id])

    def remove_callback(self, callback, sbp_msg_id):
        """
        Remove a callback.

        Args:
            callback (func): Callback function to be removed.
            sbp_msg_id (int): ID of the message.
        """
        if self._ser_handler:
            self._ser_handler.remove_callback(callback, sbp_msg_id)
        self._callbacks.remove([callback, sbp_msg_id])

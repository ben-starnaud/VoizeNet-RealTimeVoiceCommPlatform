import socket
import threading
import struct
import pyaudio
import socket
import ipaddress
import json
import ipaddress
import ast
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from conference import ConferenceCall
import servergui
import clientgui

# Initialize PyAudio parameters
CHANNELS = 1
RATE = 44100
CHUNK = 1024
clients = []

# Initialize UDP socket for client-server communication
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
IP_ADDRESS = '25.52.120.239'  # Server IP address
UDP_PORT = 1234  # Port number for UDP communication

class Client(DatagramProtocol):
    """
    This class represents a client in a VoIP conference call.
    It inherits from twisted.internet.protocol.DatagramProtocol for handling
    UDP communication.
    """

    def startProtocol(self):
        """
        This method sets up the audio input and output streams for the client
        and starts the recording thread.
        """
        py_audio = pyaudio.PyAudio()  # Initialize PyAudio
        self.buffer = 1024  # Buffer size for audio data

        # Open output stream for playing received audio
        self.output_stream = py_audio.open(format=pyaudio.paInt16,
                                           output=True, rate=44100, channels=2,
                                           frames_per_buffer=self.buffer)
        # Open input stream for recording audio
        self.input_stream = py_audio.open(format=pyaudio.paInt16,
                                          input=True, rate=44100, channels=2,
                                          frames_per_buffer=self.buffer)
        
        # Start recording thread using Twisted's reactor.callInThread method
        reactor.callInThread(self.record)

    def record(self):
        """
        This method continuously reads audio data from the input stream and
        sends it to all connected clients.
        """
        while True:
            data = self.input_stream.read(self.buffer)  # Read audio data from input stream

            # Iterate through connected clients
            for ppl in self.clients:
                # Exclude the client's own IP address to avoid sending data to itself
                if ppl != IP_ADDRESS:
                    # Send audio data to other clients using UDP
                    self.transport.write(data, (ppl, 1234))

    def datagramReceived(self, datagram, addr):
        """
        This method is called when a datagram is received.
        It writes the received audio data to the output stream.
        """
        print(datagram)  # Print received datagram for debugging purposes
        self.output_stream.write(datagram)  # Write received audio data to output stream

def execute(memb):
    """
    This function initializes the client, assigns the list of clients to the
    Client class, and starts the Twisted reactor.
    """
    port = 1234
    Client.clients = memb  # Assign list of clients to the Client class
    reactor.listenUDP(port, Client())  # Listen for UDP datagrams on the specified port
    reactor.run(installSignalHandlers=False)  # Start the Twisted reactor

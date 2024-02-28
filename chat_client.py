import socket
import threading
import struct
import conference

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDRESS = '25.52.120.239'
PORT = 12345

def receive_messages():
    message = b''
    chunk = client.recv(4) 
    expected_length = int.from_bytes(chunk, byteorder='big')
    print(expected_length)
    if expected_length != 0:
        while True:
            chunk = client.recv(1024)
            message += chunk
            if len(message) >= expected_length:
                break
        message_type = message[:4]
        message_data = message[4:]
        #print(message)
        return message_type,message_data

def start_client():
    client.connect((IP_ADDRESS,PORT))

def send_message(message):
    client.sendall(message)




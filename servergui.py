import socket
import threading
import traceback
import pyaudio
import socketserver
import customtkinter
from conference import ConferenceCall

clients = {}
calls = []
users = []
ips = []
audio = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP_ADDRESS = '25.52.120.239'
PORT = 12345
UDP_PORT = 1234



def handle_client(client_socket, client_address,app):
    while True:
            message = b''
            length = client_socket.recv(4)
            sender_ip,__port__ = client_socket.getpeername()
            
            if length != b'':
                length = int.from_bytes(length, byteorder='big')
                
                print(length)
                while True:
                    chunk = client_socket.recv(1024)
                    message += chunk
                    if len(message) >= length:
                        break
                print(message)
                message_type = message[:4].decode('utf-8')
                if message_type == 'user':
                    message = message[4:].decode('utf-8')
                    print("First 4 characters:", message_type)
                    print("ASCII values:", [ord(c) for c in message_type])
                    users.append(message)
                    update_online_users(app,users)
                    print_users()
                    message = b'logi' + message.encode('utf-8')
                    message = length.to_bytes(4, byteorder='big') + message
                    print(message)
                    broadcast(client_socket,message, sender_ip=sender_ip, conflag=False)
                elif (message_type == 'voic') or (message_type == 'text'):
                    message = length.to_bytes(4, byteorder='big') + message
                    broadcast_thread = threading.Thread(target=broadcast(client_socket, message, sender_ip=sender_ip, conflag=False))
                    broadcast_thread.start()


                elif message_type == 'disc':
                    message = message[4:].decode('utf-8')
                    remove_client(client_socket,message,app)
                    update_online_users(app, users)
                    message = b'logu' + message.encode('utf-8')
                    message = length.to_bytes(4, byteorder='big') + message
                    broadcast(client_socket,message, sender_ip=sender_ip, conflag=False)
                elif message_type == 'conf':
                    added = False
                    ul = message[4:8]
                    ul = int.from_bytes(ul, 'big')
                    ip = message[8:8+ul].decode()
                    message = message[8+ul:].decode()
                    message = [s.strip() for s in message.split(",")]
                    new_conf = ConferenceCall(name=message,limit=999)
                    
                    for call in calls:
                        for mem in call.members:
                            for p in message:
                                if p == mem:
                                    call.remove_member(mem)
                    for ppl in message:
                        if ppl == "":
                             pass
                        else:
                            new_conf.add_member(ppl)
                    calls.append(new_conf)
                    message = b'list'
                    for memb in new_conf.members:
                         message = message +b',' + memb.encode('utf-8')
                         print(message)
                    lengte = (len(message))
                    message = lengte.to_bytes(4, byteorder='big') + message
                    broadcast(client_socket,message,sender_ip=sender_ip, conflag=True)
                else:
                    remove_client(client_socket)


def broadcast(client_socket, message, sender_ip, conflag):
    print(sender_ip)
    for call in calls:
         print(call.members)
         for mem in call.members:
              if mem == sender_ip:
                print(mem)
                for ppl in call.members:
                    if ppl != sender_ip or conflag:
                          print(ppl,sender_ip)
                          print(message)
                          clients[(ppl)].sendall(message)


def remove_client(client_socket,user,self):
    if client_socket in clients:
        clients.remove(client_socket)
    if user in users:
       users.remove(user)
    add_msg(app,'f"{client_address} disconnected"')
         

def start_server(app):
    server.bind((IP_ADDRESS, PORT))
    server.listen(5)
    add_msg(app,f"Server started on {IP_ADDRESS}:{PORT}")
    print(f"Server started on {IP_ADDRESS}:{PORT}")
    #update_online_users(app,users)

    while True:
        client_socket, client_address = server.accept()
        ip,__port__ = client_address
        print(ip)
        clients[ip] = client_socket
        print(f"{client_address} connected")
        add_msg(app,'f"{client_address} connected"')
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address,app))
        client_thread.start()
        

def print_users():
    for name in users:
        print(name)

def add_msg(self, message):
        text_message = message + "\n"
        end = len(text_message)

        self.msg_index += 1
        index = str(self.msg_index)
        index = index+".0"
        self.textbox.configure(state="normal")
        self.textbox.insert(index,text=text_message)
        self.textbox.configure(state="disabled")

def update_online_users(self, users):
    text_message = ""

    for item in users:
            text_message += item+"\n"
    
    self.online_users.configure(text = text_message)




class launch_Login_panel(customtkinter.CTk):
    width = 600
    height = 600
    
    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.title("StellenTalk_Server") #naam van die window
            self.geometry(f"{self.width}x{self.height}")
            self.msg_index = 0
            self.server_frame = customtkinter.CTkFrame(self, corner_radius=20)
            self.server_frame.grid(row=0, column=0, sticky="ns")
            self.server_frame.columnconfigure(1,weight=1)
            self.server_frame.rowconfigure(2, weight=1)

            self.login_label1 = customtkinter.CTkLabel(self.server_frame,text="Server Output",font=customtkinter.CTkFont(size=30))
            self.login_label1.grid(row=0, column=0, padx=130, pady=(20, 10))

            self.textbox = customtkinter.CTkTextbox(self.server_frame,width=435, height=540, corner_radius=20,
                                                    scrollbar_button_color="dodger blue",font=customtkinter.CTkFont(size=15))
            self.textbox.grid(row=1, column=0, sticky="ns")

            self.OnlineUserslabel = customtkinter.CTkLabel(self.server_frame,text="Online Users:", anchor="center",font=customtkinter.CTkFont(size=20))
            self.OnlineUserslabel.grid(row=0, column=1, padx=(10, 10), pady=(20, 10))

            self.online_users = customtkinter.CTkLabel(self.server_frame,text="", anchor="center")
            self.online_users.grid(row=1, column=1, padx=(40, 40), pady=(20, 10), sticky="n")


if __name__ == "__main__":

        app = launch_Login_panel()
        
        start_thread = threading.Thread(target=start_server, args=(app,))
        start_thread.start()
        app.mainloop()
    
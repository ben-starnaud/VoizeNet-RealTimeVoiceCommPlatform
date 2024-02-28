import customtkinter as ctk
import os
from PIL import Image
import chat_client
import threading
from chat_client import *
import pickle
import sounddevice as sd
import numpy as np
import sys
import vn
import struct
from datetime import datetime
from moviepy.editor import *
import subprocess
from moviepy.audio.AudioClip import AudioArrayClip
import pyaudio
import wave
import vc_client
import ast
import json
import multiprocessing
from twisted.internet import reactor, protocol

class launch_Login_panel(ctk.CTk):
    width = 1080
    height = 720
    global users
    global memb
    memb = []
    users = []


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("StellenTalk") #naam van die window
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)

        # load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        self.onlyLogo = ctk.CTkImage(Image.open(os.path.join(current_path, "test_images/NewStellentalk.png")), size=(450, 175))
        self.bg_image = ctk.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),size=(self.width, self.height))
        self.reset_bg_image = ctk.CTkImage(Image.open(current_path + "/test_images/bg_gradient.jpg"),size=(1,1))
        self.bg_image_label = ctk.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = ctk.CTkFrame(self, corner_radius=20)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = ctk.CTkLabel(self.login_frame,text=""
                                                  ,image=self.onlyLogo)
        self.login_label.grid(row=0, column=0, padx=130, pady=(70, 80))

        self.username_entry = ctk.CTkEntry(self.login_frame, width=200, placeholder_text="Please enter your username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(10, 15))

        self.login_button = ctk.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=3, column=0, padx=30, pady=(15, 15))

    def receive_messages(self):
        while True:    
            #Wtry:
                message_type, data = chat_client.receive_messages()
                print(message_type + data)
                if data:
                    if message_type == b'voic':
                        print('voic')
                        message = data
                        # Save voice message to a file
                        filename = "mostrecentvnR.wav"
                        filepath = os.path.join(os.getcwd(), filename)
                        with open(filepath, 'wb') as f: 
                            f.write(message)
                        # Play voice message
                        subprocess.run(['aplay', filepath])
                    elif message_type == b'text':
                        print('text')
                        message = data
                        self.msg_index += 1
                        index = str(self.msg_index)
                        index = index+".0"
                        self.textbox.configure(state="normal")
                        self.textbox.insert(index, message.decode('utf-8'))
                        self.textbox.configure(state="disabled")
                    elif message_type == b'list':
                        message = data.decode('utf-8')
                        print()
                        message = message.split(',')
                        memb = message
                        memb = memb[1:]
                        print(memb,)
                        tr = threading.Thread(target=vc_client.execute,args=(memb,))
                        tr.start()
                    elif message_type == b'logi':
                        print(message[4:].decode('utf-8'))
                        users.append(message[4:].decode('utf-8'))
                        self.select_user._values = users
                    elif message_type == b'logu':
                        print(message[4:].decode('utf-8'))
                        users.remove(message[4:].decode('utf-8'))
                        self.select_user._values = users
                        

                    else:
                        print(message.decode('utf-8')+ " joined")

            #except Exception as e:
                #print('Error receiving message')

#The login event and all the buttons associated with it
#
#
#
    def login_event(self):
        if (self.username_entry.get() == ''):
            print("Provide username please")
        else:
            print("Login pressed - username:", self.username_entry.get())
            global client_username
            client_username = self.username_entry.get()
            self.bg_image_label.configure(self, image=self.reset_bg_image)
            self.login_frame.grid_remove()  # removel login frame
            # show main frame
            self.main()
            chat_client.start_client()
            chat_thread = threading.Thread(target = self.receive_messages)
            chat_thread.start()
            message = client_username.encode('utf-8')
            message_type = b'user'
            message = message_type + message
            data = len(message).to_bytes(4, byteorder= 'big') + message
            chat_client.send_message(data)
            

    # TODO: die gaan 'n error gee
    def reattempt_login(self):
        self.login_frame.grid_forget()  # remove main frame
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame
        self.login_label = ctk.CTkLabel(self.login_frame, text="That username is taken\nTry another one",
                                                  font=ctk.CTkFont(size=15, weight="bold"))
    
    def main(self):
        self.title("StellenTalk")
        self.geometry("1100x720")
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.onlyLogo = ctk.CTkImage(Image.open(os.path.join(image_path, "OnlyLogo.png")), size=(400, 80))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                  size=(26, 26))
        
        self.mic_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image-removebg-preview.png")),
                                            size=(20, 20))
        self.phone_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "phone_light.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "phone_dark.png")), 
                                                 size=(20, 20))

        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), 
                                                       size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), 
                                                       size=(20, 20))
        self.home_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")), 
                                                 size=(20, 20))
        self.chat_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")), 
                                                 size=(20, 20))
        self.add_user_image = ctk.CTkImage(light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), 
                                                     size=(20, 20))

        # create navigation frame (DIS NOU IN DIE LINKER KANT AF)
        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nws")
        self.navigation_frame.grid_rowconfigure(6, weight=1)
        self.navigation_frame.grid_columnconfigure(1, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  StellenTalk", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        # Make the buttons and place them on the Navigation frame
        self.home_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                    text="Message",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                     hover_color=("gray70", "gray30"),
                                                   image=self.chat_image, anchor="w")
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.conference_call_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, 
                                                      text="Conference call",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), 
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.phone_image, anchor="w", command=self.init_confcall)
        self.conference_call_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, 
                                                      border_spacing=10, text="Private Call",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), 
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",command=self.init_confcall)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = ctk.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = ctk.CTkFrame(self, corner_radius=20, fg_color=("grey90","grey17"))
        self.home_frame.grid(row=0, column=1,sticky="nswe")
        self.home_frame.grid_rowconfigure(2, weight=1)
        self.home_frame.grid_columnconfigure(1,weight=1)

        self.home_label = ctk.CTkLabel(self.home_frame,text="Message",font=ctk.CTkFont(size=15))
        self.home_label.grid(row = 0, column=0)

        # create textbox and input window and send button
        self.textbox = ctk.CTkTextbox(self.home_frame,width=700, height=650, corner_radius=20,
                                                scrollbar_button_color="dodger blue",font=ctk.CTkFont(size=20))
        self.textbox.grid(row = 1, column=0, sticky="w", padx=(5,0))
        self.msg_index = 0

        self.entry_and_send_frame = ctk.CTkFrame(self.home_frame, fg_color=("grey90","grey17"))
        self.entry_and_send_frame.grid(row=2,column=0,sticky="nswe", pady = (5,0))
        self.entry_and_send_frame.columnconfigure(1,weight=1)

        self.entrybox = ctk.CTkEntry(self.entry_and_send_frame, corner_radius=15, font=ctk.CTkFont(size=15),
                                               placeholder_text="type your message", width=540)
        self.entrybox.grid(row=0,column=0, sticky="e")
        self.sendbutton = ctk.CTkButton(self.entry_and_send_frame, corner_radius=10,text="send"
                                                  , command=self.process_msg,width=100, fg_color="dodger blue", 
                                                  text_color=("gray10", "gray90"), 
                                                  hover_color=("deep sky blue"))
        
        self.sendbutton.grid(row=0,column=1,sticky="w", padx=(5,5))

        self.voice_message_button = ctk.CTkButton(self.entry_and_send_frame, corner_radius=10,text=""
                                            , command=self.send_voice_message,width=50, fg_color="dodger blue", 
                                            text_color=("gray10", "gray90"), 
                                            hover_color=("deep sky blue"), image=self.mic_image)
        
        self.voice_message_button.grid(row=0,column=1,sticky="e",padx=(5,5))

        self.home_label = ctk.CTkLabel(self.home_frame,text="Online Users:",font=ctk.CTkFont(size=15))
        self.home_label.grid(row = 0, column=1, ipadx = 20)

        # online users and dropdown menue
        self.online_users_frame = ctk.CTkFrame(self.home_frame, corner_radius=20)
        self.online_users_frame.grid(row=1, column=1, sticky="nwes")
        # self.online_users = customtkinter.CTkLabel(self.online_users_frame,text = "jan\npiet\nkoos", corner_radius=20,font=customtkinter.CTkFont(size=20))
        # self.online_users.grid(sticky="n",padx=35)
        self.select_user = ctk.CTkComboBox(self.online_users_frame, values=users)
        self.select_user.grid(row=1, column=1, sticky="n", pady =(20, 10))
        self.private_call_button= ctk.CTkButton(self.online_users_frame, corner_radius=10,text="Call"
                                                  , command=self.process_msg,width=150, fg_color="dodger blue", 
                                                  text_color=("gray10", "gray90"), 
                                                  hover_color=("deep sky blue"))
        self.private_call_button.grid(row=1, column=1, sticky="n", pady = 60)
        self.conference_call_label = ctk.CTkLabel(self.online_users_frame,text = "Conference Call", corner_radius=20,font=ctk.CTkFont(size=18))
        self.conference_call_label.grid(row = 2, column=1, sticky="sew")
        self.conference_callentrybox = ctk.CTkEntry(self.online_users_frame, corner_radius=15, font=ctk.CTkFont(size=15),
                                               placeholder_text="Room Name", width=90)
        self.conference_callentrybox.grid(row=3,column=1, sticky="ew", padx = 15, pady=(0, 10))

        self.create_room_button = ctk.CTkButton(self.online_users_frame,text="Create/Join Room", corner_radius=10
                                            ,width=100, fg_color="dodger blue", 
                                            text_color=("gray10", "gray90"), anchor="center",
                                            hover_color=("deep sky blue"))
        
        self.create_room_button.grid(row = 3, column=1, sticky="s", padx=(30,30), pady=(70,3))
        
        self.disconnect_button = ctk.CTkButton(self.home_frame,text="Disconnect", corner_radius=10
                                            ,command=self.disconnect_user,width=100, fg_color="dodger blue", 
                                            text_color=("gray10", "gray90"), 
                                            hover_color=("deep sky blue"))
        
        self.disconnect_button.grid(row = 2, column=1, sticky="ew", padx=(30,30), pady=(0,3))

        # TODO: send voicenotes
        # TODO: conference calls with text chat in the background

        # create second frame
        
        self.conference_call_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.conference_call_frame.grid(row=1,column=1,sticky="news")
        self.conference_call_frame.grid_rowconfigure(2, weight=1)
        self.conference_call_frame.grid_columnconfigure(1,weight=1)

        

        # create third frame
        self.third_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.third_frame.columnconfigure(1, weight=1)

        # select default frame
        self.select_frame_by_name("home")



    def record_audio(self):
        global stream
        # Continuously record audio while the application is recording
        while vn.is_recording:
            # Read data from the audio stream and append it to the recording list
            data = stream.read(chunk_size)
            vn.recording.append(data)

    def send_voice_message(self):
        global stream, chunk_size
        sample_rate = 44100
        chunk_size = 1024
        p = pyaudio.PyAudio()
        # If not recording, start recording
        if not vn.is_recording:
            vn.is_recording = True
            # Change the color of the voice message button to indicate recording
            self.voice_message_button._fg_color = 'red'
            self.voice_message_button._hover_color = 'firebrick1'
            # Open the audio stream for recording
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=chunk_size)
            vn.recording = []
            # Start a new thread for the record_audio function
            vn.thread = threading.Thread(target=self.record_audio)
            vn.thread.start()
        # If recording, stop recording
        else:
            vn.is_recording = False
            # Change the color of the voice message button back to default
            self.voice_message_button._fg_color = 'dodger blue'
            self.voice_message_button._hover_color = 'deep sky blue'
            # Stop recording and close the audio stream
            vn.thread.join()
            stream.stop_stream()
            stream.close()
            p.terminate()
            # Convert the audio data to numpy array
            audio_data = np.frombuffer(b''.join(vn.recording), dtype=np.int16).astype(np.float32) / 32768.0
            filename = "mostrecentvn.wav"
            filepath = './voicenotes/' + filename
            # Save the recorded audio to a WAV file
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(sample_rate)
            wf.writeframes(b''.join(vn.recording))
            wf.close()
            # Prepare the message to be sent, including the message type and the audio data
            message_type = b'voic'
            with open(filepath, 'rb') as f:
                message = f.read()
            message = message_type + message
            data = len(message).to_bytes(4, byteorder='big') + message
            # Start a new thread to send the voice message
            send_vn_thread = threading.Thread(target=chat_client.send_message(data))
            send_vn_thread.start()

    def disconnect_user(self):
        # Prepare the disconnect message with the client's username
        message = client_username.encode('utf-8')
        message = b'disc' + message
        data = len(message).to_bytes(4, byteorder='big') + message
        # Send the disconnect message to the server
        chat_client.send_message(data)
        # Close the application and exit
        app.destroy()
        sys.exit()

    def update_online_users(self):
        # Placeholder function for updating the list of online users
        print("temp update online users button is pressed")

    def process_msg(self):
        # Get the text message from the entry box and append the client's username
        text_message = self.entrybox.get() + '\n'
        text_message = client_username + ": " + text_message
        end = len(text_message)

        self.msg_index += 1
        index = str(self.msg_index)
        index = index + ".0"
        self.textbox.configure(state="normal")
        self.textbox.insert(index, text_message)
        message_type = b'text'
        message = text_message.encode('utf-8')
        message = message_type + message
        data = len(message).to_bytes(4, byteorder= 'big') + message
        chat_client.send_message(data)
        self.entrybox.delete(0, end)
        self.textbox.configure(state="disabled")



    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.conference_call_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.conference_call_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.conference_call_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def init_confcall(self):
        vn.leave_call = not vn.leave_call


        cul = len(chat_client.client.getsockname()[0])
        message = b'conf' + int.to_bytes(cul, 4, 'big') + (chat_client.client.getsockname()[0]).encode()
        message = message + (self.entrybox.get()).encode()
        ml = len(message)
        ml = int.to_bytes(ml, 4, 'big')
        message = ml + message
        chat_client.send_message(message=message)


    def change_appearance_mode_event(self, new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)

if __name__ == "__main__":
    app = launch_Login_panel()
    app.mainloop()

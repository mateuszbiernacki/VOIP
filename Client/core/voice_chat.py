import socket
import threading
import pyaudio


class VoiceConnection:
    def __init__(self, friend_ip):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target_ip = friend_ip
        self.target_port = 20001

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        try:
            print('a')
            data = self.recording_stream.read(512)
            print('a')
            self.s.sendto(data, (self.target_ip, self.target_port))
            print('a')
            rec_data, address = self.s.recvfrom(512)
            print('a')
            self.playing_stream.write(rec_data)
            print('a')
        except Exception as e:
            print(e)

        # start threads
        # self.receive_thread = threading.Thread(target=self.receive_server_data)
        # self.receive_thread.start()
        # self.send_data()

    def receive_server_data(self):

        while True:
            try:
                data, address = self.s.recvfrom(1024)
                self.playing_stream.write(data)
                print('ok1')
            except Exception as e:
                print(e)

    def send_data(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendto(data, (self.target_ip, self.target_port))
                print('ok2')
            except Exception as e:
                print(e)


class VoiceConnection2:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            self.s.bind(('', 20001))

        except:
            print("Couldn't bind")

        chunk_size = 1024  # 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        # initialise microphone recording
        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True,
                                          frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                            frames_per_buffer=chunk_size)

        print("Connected to Server")

        try:
            print('b')
            rec_data, address = self.s.recvfrom(1024)
            print('b')
            self.playing_stream.write(rec_data)
            print('b')
            data = self.recording_stream.read(512)
            print('b')
            self.s.sendto(data, address)
            print('b')
            print('ok1')
        except Exception as e:
            print(e)

        # start threads
        # self.receive_thread = threading.Thread(target=self.receive_server_data)
        # self.receive_thread.start()
        # self.target_ip = None
        # self.target_port = None
        # self.send_data()

    def receive_server_data(self):

        while True:
            try:
                data, address = self.s.recvfrom(1024)
                self.playing_stream.write(data)
                self.target_ip = address[0]
                self.target_port = address[1]
                print('ok1')
            except Exception as e:
                print(e)

    def send_data(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendto(data, (self.target_ip, self.target_port))
                print('ok2')
            except Exception as e:
                print(e)

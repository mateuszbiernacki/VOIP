import time

from PyQt5.QtCore import QObject, pyqtSignal
import socket
import json


class Receiver(QObject):
    finished = pyqtSignal()
    show_friend_request = pyqtSignal(str)

    def run(self):
        while True:
            time.sleep(20)
            print('a')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print('a')
            sock.bind(('localhost', 2137))
            print('a')
            data, address = sock.recvfrom(1024)
            print('a')
            response = json.loads(data.decode('utf-8'))
            print('a')
            if response['short'] == "s_inv_to_friends":
                self.show_friend_request.emit(response["friend_login"])
        # for i in range(4):
        #     time.sleep(1)
        #     self.progress.emit('test', 'test')
        # self.finished.emit()

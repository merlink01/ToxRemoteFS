from tox_api import *
import Queue
import json
import time
import threading
import uuid
import logging
import sys


class Client(Tox_Worker):

    def listdir(self,*args,**kwargs):

        data = {}
        data['command'] = 'listdir'
        data['args'] = args
        data['kwargs'] = kwargs
        data['uuid'] = str(uuid.uuid4())

        jdata = json.dumps(data)
        self.logger.debug(jdata)
        self.friend_send_message(0,jdata)
        while not data['uuid'] in self.recieve_data:
            time.sleep(0.001)
        self.recieve_lock.acquire()
        outdata = self.recieve_data[data['uuid']]
        del self.recieve_data[data['uuid']]
        self.recieve_lock.release()
        self.logger.debug(str(outdata))
        if outdata is None:
            self.logger.error('Server Error')
            self.logger.error(str(data))
        return outdata


    def getinfo(self,path):
        data = {}
        data['command'] = 'getinfo'
        data['args'] = (path)
        data['kwargs'] = {}
        data['uuid'] = str(uuid.uuid4())

        jdata = json.dumps(data)
        self.logger.debug(jdata)
        self.friend_send_message(0,jdata)
        while not data['uuid'] in self.recieve_data:
            time.sleep(0.001)
        self.recieve_lock.acquire()
        outdata = self.recieve_data[data['uuid']]
        del self.recieve_data[data['uuid']]
        self.recieve_lock.release()
        self.logger.debug(str(outdata))
        if outdata is None:
            self.logger.error('Server Error')
            self.logger.error(str(data))
        return outdata

    def isdir(self,path):
        data = {}
        data['command'] = 'isdir'
        data['args'] = (path)
        data['kwargs'] = {}
        data['uuid'] = str(uuid.uuid4())

        jdata = json.dumps(data)
        self.logger.debug(jdata)
        self.friend_send_message(0,jdata)
        while not data['uuid'] in self.recieve_data:
            time.sleep(0.001)
        self.recieve_lock.acquire()
        outdata = self.recieve_data[data['uuid']]
        del self.recieve_data[data['uuid']]
        self.recieve_lock.release()
        self.logger.debug(str(outdata))
        if outdata is None:
            self.logger.error('Server Error')
            self.logger.error(str(data))
        return outdata


    def isfile(self,path):
        data = {}
        data['command'] = 'isfile'
        data['args'] = (path)
        data['kwargs'] = {}
        data['uuid'] = str(uuid.uuid4())

        jdata = json.dumps(data)
        self.logger.debug(jdata)
        self.friend_send_message(0,jdata)
        while not data['uuid'] in self.recieve_data:
            time.sleep(0.001)
        self.recieve_lock.acquire()
        outdata = self.recieve_data[data['uuid']]
        del self.recieve_data[data['uuid']]
        self.recieve_lock.release()
        self.logger.debug(str(outdata))
        if outdata is None:
            self.logger.error('Server Error')
            self.logger.error(str(data))
        return outdata

    def send_command(self,command,code):

        data = {}
        data['command'] = command
        data['code'] = code
        data['uuid'] = str(uuid.uuid4())

        jdata = json.dumps(data)

        self.friend_send_message(0,jdata)
        while len(self.recieve_queue.queue) == 0:
            time.sleep(1)
        return json.loads(self.recieve_queue.get()[1])

    def connect_to_slave(self,serverID, passwd):
        self.logger.info('Connecting to Slave')
        num = self.friend_add(serverID, passwd)
        while self.friend_get_connection_status(num) is not True:
            time.sleep(0.1)
        self.logger.info('Done')

    def on_friend_message(self, serverID, message):
        data = json.loads(message)
        self.recieve_lock.acquire()
        self.recieve_data[data[0]] = data[1]
        self.recieve_lock.release()

    def callback_start(self):
        self.logger = logging.getLogger('TOXFSCLIENT')
        self.recieve_data = {}
        self.recieve_lock = threading.Lock()

    def on_file_recv(self, serverID, *args):
        pass

    def on_file_recv_control(self, serverID, *args):
        pass

    def callback_round(self):
        pass

    def on_friend_request(self, pk, message):
        pass

PASSWORD = 'Commandserver'


class FS_Client():
    def __init__(self):

        sets = Settings('settings/master.bin','Master')
        self.controller = Controller(Client,sets)

    def start(self):
        self.controller.start()
        time.sleep(2)
        self.controller.tox.connect_to_slave('4B5F05366439C7477F79AE0C8CA9F94FA30AFF8F751D86D059557072B0697C3C65D338035E6E',PASSWORD)

    def stop(self):
        self.controller.stop()

    def listdir(self,*args,**kwargs):
        return self.controller.tox.listdir(*args,**kwargs)

    def isfile(self,path):
        return self.controller.tox.isfile(path)

    def isdir(self,path):
        return self.controller.tox.isdir(path)

    def getinfo(self,path):
        return self.controller.tox.getinfo(path)

logger = logging.getLogger()
fmt_string = "[%(levelname)-7s]%(asctime)s.%(msecs)-3d\
%(module)s[%(lineno)-3d]/%(funcName)-10s  %(message)-8s "
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(logging.Formatter(fmt_string, "%H:%M:%S"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

a = FS_Client()
a.start()
ld = a.listdir()
for x in ld:
    print x, a.isfile(x),a.isdir(x),a.getinfo(x)


a.stop()


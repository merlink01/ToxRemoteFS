import os
import pickle
import logging
logger = logging.getLogger('Settings')

class ToxOptions():
    def __init__(self):
        self.name = 'Unnamed'
        self.ipv6_enabled = False
        self.udp_enabled = False
        self.proxy_type = 0 # 1=http, 2=socks
        self.proxy_host = ''
        self.proxy_port = 0
        self.start_port = 0
        self.end_port = 0
        self.tcp_port = 0
        self.savedata_type = 1 # 1=toxsave, 2=secretkey
        self.savedata_data = b''
        self.savedata_length = 0

class Settings():
    def __init__(self,path=None,name=None):
        if not name:
            name = 'Unnamed'
        if not path:
            path = os.path.abspath('settings.bin')


        if not os.path.dirname(path) == '':
            if not os.path.exists(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))

        self.name = name
        self.path = path

    def save(self,data,length,name):
        logger.debug('Save to %s'%self.path)
        savedata = ToxOptions()
        savedata.name = self.name
        savedata.savedata_data = data
        savedata.savedata_length = length
        pickle.dump( savedata, open(self.path, 'wb' ) )

    def read(self):
        logger.debug('Read from %s'%self.path)
        if not os.path.isfile(self.path):
            print('Save not exists')
            return ToxOptions()
        logger.debug('Done')
        return pickle.load( open( self.path, "rb" ) )

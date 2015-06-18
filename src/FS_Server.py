import os
import sys
import json
import logging
import traceback
import StringIO
from tox_api import *

class FS_Server(Tox_Worker):

    def on_friend_request(self, pk, passwd):
        self.logger.info('Login: %s'%pk)
        self.logger.info('Passwd: %s'%passwd)
        if passwd == PASSWORD:
            self.friend_add_norequest(pk)
            self.logger.info('Allowed')
        else:
            self.logger.warning('Forbidden: %s'%pk)


    def execute(self, friendId, message):
        data = json.loads(message)
        try:
            retval = None

            self.logger.debug('From: %s'%friendId)
            self.logger.info('Command: %s'%(data['command']))
            self.logger.debug('Command: %s %s %s'%(data['command'],
                                str(data['args']), str(data['kwargs'])))

            if 'path' in data['kwargs']:
                data['kwargs']['path'] = os.path.join(ROOTPATH , data['kwargs']['path'])

            if data['command'] == 'listdir':
                #Todo Parameter

                if len(data['args']) == 0:
                    path = ROOTPATH
                else:
                    path = ROOTPATH  + data['args'][0]

                retval = os.listdir(path)

            if data['command'] == 'isfile':
                retval = os.path.isfile(os.path.join(ROOTPATH, data['args'][0]))

            if data['command'] == 'isdir':
                retval = os.path.isdir(os.path.join(ROOTPATH,data['args'][0]))

            if data['command'] == 'rename':
                os.rename(os.path.join(ROOTPATH,data['args'][0],os.path.join(ROOTPATH,data['args'][1])))
                retval = True

            if data['command'] == 'remove':
                os.remove(os.path.join(ROOTPATH,data['args'][0]))
                retval = True

            if data['command'] == 'removedir':
                #params
                os.rmdir(os.path.join(ROOTPATH,data['args'][0]))
                retval = True

            if data['command'] == 'makedir':
                #params
                os.mkdir(os.path.join(ROOTPATH,data['args'][0]))
                retval = True

            if data['command'] == 'getinfo':
                path = os.path.join(ROOTPATH,data['args'][0])
                stat = os.stat('FS_Server.py')
                filestat = {}
                filestat['size'] = stat.st_size
                filestat['created_time'] = stat.st_ctime
                filestat['accessed_time'] = stat.st_atime
                filestat['modified_time'] = stat.st_mtime
                retval = filestat

            retval = (data['uuid'],retval)

            self.logger.debug('Return: %s'%str(retval))
            self.friend_send_message(friendId, json.dumps(retval))
        except:
            tmp = StringIO.StringIO()
            traceback.print_exc(file=tmp)
            tmp.seek(0, 0)
            self.logger.error(tmp.read())
            tmp.close()
            retval = (data['uuid'],None)
            self.friend_send_message(friendId, json.dumps(retval))

    def on_friend_message(self, *args):
        self.execute(*args)

    def on_file_recv(self, friendId, *args):
        pass

    def on_file_recv_control(self, friendId, *args):
        pass

    def callback_round(self):
        pass

if __name__ == '__main__':

    logger = logging.getLogger()
    fmt_string = "[%(levelname)-7s]%(asctime)s.%(msecs)-3d\
    %(module)s[%(lineno)-3d]/%(funcName)-10s  %(message)-8s "
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(fmt_string, "%H:%M:%S"))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


    PASSWORD = 'Commandserver'
    ROOTPATH = '/home/user/test'

    if not os.path.exists(ROOTPATH):
        os.makedirs(ROOTPATH)

    sets = Settings('settings/slave.bin','Slave')

    c = Controller(FS_Server,sets)
    c.start()
    try:
        import time
        while 1:
            time.sleep(100)
    except KeyboardInterrupt:
        c.stop()


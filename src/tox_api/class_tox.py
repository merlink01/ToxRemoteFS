import pytox
import time
import class_servers
import logging
import sys

class Tox_Worker(pytox.Tox):

    def connect(self):
        if self.self_get_connection_status():
            self.logger.debug('Unneeded Connection attempt')
            return True
        for SERVER in class_servers.get_servers():
            self.logger.debug('Try Connection to Server %s'%str(SERVER))
            self.bootstrap(SERVER[0], SERVER[1], SERVER[2])
            timeout = 1000
            while timeout >= 0:
                timeout -= 1
                self.iterate()
                time.sleep(0.01)
                if self.self_get_connection_status():
                    self.logger.debug('Connected')
                    return True
            self.logger.debug('Timeout reached')


    def loop(self):
        self.callback_start()
        self.logger.debug('Starting Tox Loop')
        self.connect()
        checked = False
        try:
            while True:
                status = self.self_get_connection_status()

                if not checked and status:
                    self.logger.info('Connected to DHT')
                    checked = True

                if checked and not status:
                    self.logger.info('Disconnected from DHT')
                    self.connect()
                    checked = False

                self.iterate()

                time.sleep(0.01)
                self.callback_round()
        except KeyboardInterrupt:
            self.logger.info('Keyboard Interrupt recieved, shutting down...')
            self.kill()
            sys.exit(0)

    def callback_round(self):
        pass

    def callback_start(self):
        self.logger = logging.getLogger('Tox_Worker')


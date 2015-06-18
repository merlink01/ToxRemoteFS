import time
import logging
import threading
logger = logging.getLogger('Controller')

class Controller():

    def __init__(self, worker_obj, settings_obj, name=None):
        logger.info('Starting Tox Controller')

        self.tox = worker_obj(settings_obj.read())
        settings_obj.save(self.tox.get_savedata(),self.tox.get_savedata_size(),name)

        self.tox.self_set_name("VFS_Server")
        logger.info('TOX_ID: %s' % self.tox.self_get_address())
        self.running = False

    def start(self):
        if self.tox.self_get_connection_status():
            logger.warning('Server is already running')

        t = threading.Thread(target=self.tox.loop)
        t.daemon = True
        t.start()

        while not self.tox.self_get_connection_status():
            time.sleep(0.01)

    def stop(self):
        self.tox.kill()
        logger.info('Shutdown Correct')





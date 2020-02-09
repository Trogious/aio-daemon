import os
import sys
import time

from aio_daemon import Daemon


class TestDaemon(Daemon):
    def run(self, loop):
        self.logger.info('overriden run')
        loop.stop()


class TestDaemon2(Daemon):
    async def run_task(self):
        self.logger.info('overriden run: task')

    def run(self, loop):
        loop.create_task(self.run_task())
        loop.stop()


class TestDaemon3(Daemon):
    async def run_task(self):
        self.logger.info('overriden run: task')

    def run(self, loop):
        pass

    def run_loop(self, loop):
        self.logger.info('overriden run_loop')
        loop.run_until_complete(self.run_task())


if __name__ == '__main__':

    pid = os.fork()
    if pid < 0:
        print('fork failed: %d' % pid)
        sys.exit(1)
    elif pid == 0:
        d = TestDaemon()
        d.start()
        d = TestDaemon2()
        d.start()
        d = TestDaemon3()
        d.start()
    else:
        time.sleep(1)
        logfile = './aio_daemon.log'
        try:
            with open(logfile, 'r') as f:
                print(f.read())
            os.remove(logfile)
        except FileNotFoundError as e:
            print(e)

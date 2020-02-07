import asyncio
import os
import signal
import sys

from .env import getenv_path
from .logging import Logger


class Daemon:
    AIO_DAEMON_PID_PATH = './aio_daemon.pid'

    def __init__(self):
        self.logger = Logger.get_logger()
        self.pid_path = getenv_path('AIO_DAEMON_PID_PATH', Daemon.AIO_DAEMON_PID_PATH)
        self.pid = 0

    async def handle_signal2(self, loop, signum):
        self.logger.info('signal received: %d' % signum)
        loop.stop()

    def create_pid(self):
        try:
            with open(self.pid_path, 'w') as f:
                self.pid = os.getpid()
                f.write(str(self.pid))
                f.flush()
        except Exception as e:
            self.logger.error('cannot create PID file: ' + self.pid_path)
            self.logger.debug(e)

    def delete_pid(self):
        try:
            os.remove(self.pid_path)
        except Exception as e:
            self.logger.error('removing PID file failed: ' + self.pid_path)
            self.logger.debug(e)

    def daemonize(self):
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
        elif pid < 0:
            self.logger.error('fork failed: %d' % pid)
            sys.exit(1)
        os.chdir('/')
        os.setsid()
        os.umask(0)
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()

    def start(self):
        self.daemonize()
        self.create_pid()
        loop = asyncio.get_event_loop()
        for s in [signal.SIGINT, signal.SIGUSR1, signal.SIGTERM]:
            loop.add_signal_handler(s, lambda s=s: loop.create_task(self.handle_signal2(loop, s)))
        try:
            self.run(loop)
            self.logger.debug('run() executed')
            loop.run_forever()
        except OSError as e:
            self.logger.error(e.filename, exc_info=e)
        except Exception as e:
            self.logger.error(e)
        finally:
            self.delete_pid()

    # abstract method to override in subclasses
    def run(self, loop):
        raise NotImplementedError('run() needs to be overriden in a subclass')

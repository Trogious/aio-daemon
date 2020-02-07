from aio_daemon import Daemon


class TestDaemon(Daemon):
    def run(self, loop):
        self.logger.info('overriden run')
        loop.stop()


d = TestDaemon()
d.start()

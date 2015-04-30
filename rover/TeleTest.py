import sys
sys.dont_write_bytecode = True


from threads.telemetryThread import telemetryThread

import time

class TeleTest():
        def __init__(self):
                self.telemetryThread = telemetryThread(self)

        def stopThreads(self):
                self.telemetryThread.stop()
                
        def startThreads(self):
                print("starting threads")
                self.telemetryThread.start()

        def run(self):
                self.startThreads()
                # go until error
                try:
                        while True:
                                pass
                except KeyboardInterrupt:
                        print("stopping")
                        self.stopThreads()
                except:
                        self.stopThreads()
                        raise

app = TeleTest()
app.run()


import threading
import time

class MyThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._quit_flag = False
    def run(self):
        while not self._quit_flag:
            print("Thread is alive!")
            time.sleep(0.500)
        print("shutting down.")
    def request_quit(self):
        self._quit_flag = True

mt = MyThread()
mt.start()

# Shutdown thread
threading.Thread(
    target=lambda: threading.main_thread().join() or mt.request_quit()
    ).start()
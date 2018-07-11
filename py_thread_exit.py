import threading
import signal
import os
import time

def handle(signum,frame):
    print "fuck!!"
    print signum
    os._exit(0)

def func():
    signal.signal(signal.SIGINT,handle)
    print "hello!!!"
    while 1:
        time.sleep(1)
        





P1 = threading.Thread(target = func)

P1.start()
P1.join()
print "fuck!!!!!"
while 1:
    pass


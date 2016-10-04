# -*- coding: utf-8 -*-
# todo
# write multitascing decorator library
import threading

class Thread(object):
    
    def __init__(self):
        self.threads = []
        
    def __call__(self, f):
        t = threading.Thread(target=f)
        t.daemon = True
        self.threads.append(t)
        t.start()

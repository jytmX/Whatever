# -*- coding: utf-8 -*-
import requests,socket
requests.packages.urllib3.disable_warnings()
from threading import *
from threading import Thread
from ConfigParser import ConfigParser
from Queue import Queue

class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        self.tasks.join()

def main(url):
 if "://" in url:
      url = url
 else:
	  url = "http://"+url
 if url.endswith('/'):
	  url = url[:-1]
 try:
		r = requests.get(url)
		print(r.url)
		simpan = open('urlnew.txt', 'a')
		simpan.write(r.url+'\n')
		simpan.close()
 except:
		pass

print("""
         coco

""")
readsplit = open(raw_input("Ips List .txt: "), 'r').read().splitlines()
numthread = raw_input("Thread: ")
pool = ThreadPool(int(numthread))
for url in readsplit:
 
 pool.add_task(main, url)


pool.wait_completion()

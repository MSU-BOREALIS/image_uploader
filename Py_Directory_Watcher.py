# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:43:43 2016

@author: Trevor Gahl
"""
#import os
import sys
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from auth import authenticate
from upload import upload_kitten


client = authenticate()


"""
Directory Watcher
"""


 
class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.png"]

    def process(self, event):        
        # the file will be processed there
        print event.src_path, event.event_type  # print now only for degug

    def on_modified(self, event):
        self.process(event)
        print "File Modified"

    def on_created(self, event):
        self.process(event)
        image = upload_kitten(client, event.src_path)
        print("Image was posted! Go check your images you sexy beast!")
        print("You can find it here: {0}".format(image['link']))
        
if __name__ == '__main__':
    args = sys.argv[1:]
    observer = Observer()
    observer.schedule(MyHandler(), path=args[0] if args else 'C:\Users\Trevor\Documents')
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    
    

 
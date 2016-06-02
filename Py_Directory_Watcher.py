# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:43:43 2016

@author: Trevor Gahl
"""
import sys
import time

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from auth import authenticate
from upload import upload_kitten

#Authorizes connection with Borealis Imgur account
client = authenticate()


"""
Directory Watcher and Imgur Uploader
"""


#Creates a handler capable of matching patterns to watch the directory 
class MyHandler(PatternMatchingEventHandler):
    #Checks for any file with a .jpg or .png file extension
    patterns = ["*.jpg", "*.png"]

    def process(self, event):        
        print event.src_path, event.event_type  # print now only for degug

    #Checks if a file has been modified
    def on_modified(self, event):
        self.process(event)
        print "File Modified"

    #Checks if a file has been created
    def on_created(self, event):
        self.process(event)
        #If a new file was created it uploads the photo to the Borealis Imgur account
        image = upload_kitten(client, event.src_path)
        print("Image was posted!")
        print("You can find it here: {0}".format(image['link']))
        
if __name__ == '__main__':
    
    observer = Observer()
    #Modify path in following line of code to where the pictures will be stored.
    observer.schedule(MyHandler(), path='C:\Users\Trevor\Documents', recursive = True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
    
    

 
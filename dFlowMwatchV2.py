import csv
import logging
import random

from tools import confreader
import sys
import time,datetime
#from dataFlowWatch import Handler
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler,FileSystemEventHandler
from collections import namedtuple
from tools import  removeOldRecords
config= namedtuple("config","isEnable pointTag directory interval")
watchDictFile= 'work/dFlowDictV2.csv'


def getTagByPath(path, config):
    for k in range(len(config.pointTag)):
        # print(config.directory[k])
        if config.directory[k] in path: return config.pointTag[k]
    return print("cannot find : ", dir)
    pass


class Handler(FileSystemEventHandler):
    @staticmethod

    @staticmethod
    def on_any_event(event):
        watchDict = dict()
        if event.is_directory:

            return None
        else :

            time.sleep(0.0001) #for different key generating
            config= confreader()
            ###################
            tag='empty'
            for k in range(len(config.pointTag)):
                # print(config.directory[k])
                if config.directory[k] in event.src_path: tag= config.pointTag[k]
            #####################
            key=str( datetime.datetime.now())+"@"+ tag+ "@"+event.src_path+"@" + str(random.randint(1000,9999))
            watchDict[key]=event.event_type
            with open(watchDictFile, 'a', newline='') as csv_file:
            #     writer = csv.writer(csv_file)
            #     for key, value in watchDict.items():
            #         writer.writerow([key, value])
              w = csv.writer(csv_file)
              w.writerows(watchDict.items())

        def getTagByPath(path, config):

            for k in range(len(config.pointTag)):
                # print(config.directory[k])
                if config.directory[k] in path: return config.pointTag[k]
            return print("cannot find : ", dir)

##########################################

################################################
# Attach a logging event AKA FileSystemEventHandler
event_handler = Handler()

# Create Observer to watch directories
observer = Observer()
conf=confreader()

# Take in list of paths. If none given, watch CWD
paths = conf.directory

# Empty list of observers
observers = []

# Base logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Iterate through paths and attach observers
for targetPath in paths:
    # Schedules watching of a given path
    observer.schedule(event_handler, targetPath,recursive=True)

    # Add observable to list of observers
    observers.append(observer)
    print (f"observer for {targetPath} is running")

# Start observer
observer.start()

try:
    while True:

        # Poll every second
        time.sleep(1)

except KeyboardInterrupt:
    for o in observers:
        o.unschedule_all()

        # Stop observer if interrupted
        o.stop()

for o in observers:

    # Wait until the thread terminates before exit
    o.join()

import unittest, time, re
import os
import time
from .FileWatch import FileWatch

class ManageWatchDirestory:
    ###
    # Mange the Watch scenario of the application
    # ###
    def __init__(self,logsDirectory):
        self.logsDirectory = logsDirectory
    def WatchDirectory(self,total_time,period_time):
        ###
        # run on total time to watch files and every period_time look on the files to sdee changes
        #period_time in minutes
        #total_time in minutes
        ###
        watch = FileWatch(self.logsDirectory)
        periodtime = period_time;
        totaltime = total_time * 60
        print('Start Watching Directory for total Time {0} in Minutes'.format(total_time))
        print('Ther is cycle of {0} Seconds each time'.format(period_time))
        while totaltime > 0:
            count = 0
            watch.WatchingChange()
            while periodtime >= count:
                time.sleep(1)
                count += 1
                totaltime -= 1

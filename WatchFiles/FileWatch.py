import fnmatch
import glob
import os
from datetime import datetime
class FileWatch():
    ###
    # Manage watching the Directory
    # ###
    def __init__(self,logsDirectory):
        self.logfiles = {}
        self.logsDirectory = logsDirectory
        # if not self.logsDirectory.endswith('/'):
        #     self.logsDirectory = self.logsDirectory + '/'
        if not os.path.exists(self.logsDirectory):
            os.makedirs(self.logsDirectory)
    def GetDateTime(self):
        ###
        # Return the Date Time in format of israel tiem
        # ###
        now = datetime.now()  # current date and time
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        return date_time
    def WatchingChange(self):
        ###
        # Move to watch directory as self.logsDirectory and look on dirty files, add them to list ,mark them as dirty and delete them
        # For clean files mark them as add amd then see if there is a change in update tiem of the file and marked it as changed
        # ###
        try:
            start = False;
            if len(self.logfiles) == 0:
                start = True
            os.chdir(self.logsDirectory)
            dirs = os.listdir()
            dirtyfiles = [x for x in dirs if x.find(".dirty") > 0]

            diertyfileslen = len(dirtyfiles)
            if diertyfileslen > 0:
                print('There are {0} Dirty files in directory'.format(diertyfileslen))

            for f in dirtyfiles:
                print('{0}::!{1}!::{2}'.format(self.GetDateTime(),'ADDED',f))
                print('{0}::!{1}!::{2}'.format(self.GetDateTime(),'DIRTY',f))
            for f in dirtyfiles:
                try:
                    os.remove(f)
                    print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'REMOVED', f))
                except Exception as ex:
                    print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'ERROR', f))
            dirs = os.listdir()
            dirtyfiles = [x for x in dirs if x.find(".dirty") > 0]
            diertyfileslen = len(dirtyfiles)
            if diertyfileslen > 0:
                print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'ERROR', 'Application failed to remove dirty files'))
            logfiles = [x for x in dirs if x.find(".dirty") < 0]
            for f in logfiles:
                if '.dirty' in f:
                    continue
                if start == False:
                    # We all ready watch the files
                    if f in self.logfiles:
                        lasttime = self.logfiles[f]
                        current = os.path.getmtime(f)
                        if  current != lasttime:
                            print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'CHANGED', f))
                    else:
                        print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'ADDED', f))
                        print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'CLEAN', f))
                else:
                    # We at the start so we mark the file as clean and start watcg it changes
                    print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'ADDED', f))
                    print('{0}::!{1}!::{2}'.format(self.GetDateTime(), 'CLEAN', f))
                self.logfiles[f] = os.path.getmtime(f)
        except Exception as ex:
            template = "In FileWatch Method WatchingChange - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)



import os,time
from time import sleep
from random import randint
from shutil import copyfile,copy

class GenerateTestFiles:
###
# Class that support creating & copy files to watch directory
# and give test results for tests TestCopyFiles & TestChengesFiles
# ###
    def __init__(self,watchDirectory,totalFilesGenerate,log):
        self.watchDirectory = watchDirectory
        self.totalFilesGenerate = totalFilesGenerate
        self.log = log
        applicationStdOut = []
        self.dirtyFiles = []
        self.cleanFiles = []
        # self.mngdirectories = ManageDirectories(watchDirectory)
    def addlogline(self,line,extra='',toconsole=False):
        ###
        # Add Line to console & to log file
        # ###
        if toconsole == True:
            print(line,extra)
        self.log.AddLogLine(line+" "+extra)
    def CreateDirtyFile(self):
        ###
        # We Create Dirty File in the Watch Directory
        # We did not use this method, we use the copy method instead
        ###
        try:
            i = 56
            r = randint(i * 100, i * 10000000)
            name_d = "{0}/DirtylogFile{1}.dirty".format(self.watchDirectory,r)
            if not os.path.exists(name_d):
                with open(name_d, "w", encoding="utf-8") as f:
                    for i in range(10):
                        f.write("This is line %d\r\n" % (i + 1))
                    f.close()
            return name_d
        except Exception as ex:
            template = "In GenerateTestFiles Method CreateDirtyFile - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.addlogline(message)
            return ''
    def CreateCleanFile(self):
        ###
        # We Create Clean File in the Watch Directory
        # We did not use this method, we use the copy method instead
        ###
        try:
            i = 33
            r = randint(i * 100, i * 10000000)
            name_l = "{0}/LogFile{1}{2}.clean".format(self.watchDirectory, r)
            if not os.path.exists(name_l):
                with open(name_l, "w", encoding="utf-8") as f:
                    for i in range(10):
                        f.write("This is line %d\r\n" % (i + 1))
                    f.close()
            return name_l
        except Exception as ex:
            template = "In GenerateTestFiles Method CreateCleanFile - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.addlogline(message)
            return ''
    def EditSeveralCleanFile(self,num):
        ###
        # Edit several Clean files from the Watch Directory
        # ###
        os.chdir(self.watchDirectory)
        cahngedfiles = []
        list = os.listdir(self.watchDirectory)
        count = 0;
        self.addlogline("-------------------------------",'',False)
        self.addlogline("Files that were Changed", '', False)
        for f in list:
            if '.dirty' in f:
                continue
            cahngedfiles.append(f)
            self.addlogline(f)
            count += 1
            if count >= num:
                break
        self.addlogline("-------------------------------", '', False)
        for f in cahngedfiles:
            self.EditCleanFile(f)
            time.sleep(0.5)
        return cahngedfiles
    def EditCleanFile(self,name_l):
        ###
        # We Edit existing file
        # ###
        try:
            i = 33
            os.chdir(self.watchDirectory)
            r = randint(i * 100, i * 10000000)
            string = "\r\nAdd new data to file - {0}\r\n".format(r)
            if os.path.exists(name_l):
                with open(name_l, "w+", encoding="utf-8") as f:
                    f.write(string)
                    f.close()
            return name_l
        except Exception as ex:
            template = "In GenerateTestFiles Method EditCleanFile - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.addlogline(message)
            return ''

    def CopyFilesToWatchDirectory(self):
        ###
        # We Copy The files from dirty & clean directories to the watch directory so the application will test it
        ###
        self.dirtyFiles = []
        self.cleanFiles = []
        os.chdir(self.watchDirectory+'/dirty')
        newpath = os.getcwd()
        list = os.listdir(newpath)
        for f in list:
            if '.' in f:
                try:
                    # copyfile(f,"{0}/{1}".format(self.watchDirectory,f))
                    copy(f, "{0}/{1}".format(self.watchDirectory, f))
                    self.dirtyFiles.append(f)
                except Exception:
                    sleep(0.1)
                sleep(0.4)
        os.chdir(self.watchDirectory+'/clean')
        newpath = os.getcwd()
        list = os.listdir(newpath)
        for f in list:
            if '.' in f:
                try:
                    # copyfile(f,"{0}/{1}".format(self.watchDirectory,f) )
                    copy(f, "{0}/{1}".format(self.watchDirectory,f))

                    self.cleanFiles.append(f)
                except Exception:
                    sleep(0.1)
                sleep(0.4)
        return self.cleanFiles,self.dirtyFiles
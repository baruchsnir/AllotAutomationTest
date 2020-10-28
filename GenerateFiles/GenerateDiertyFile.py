from random import randint
import unittest
import os

from .GenerateDirtyFileWithSelenium import GenerateDirtyFileWithSelenium
class GenerateDiertyFile():
    ###
    # Class that Generate Files , The data arived from web pages by selenium
    # ##
    def __init__(self,logsDirectory,numberOfFiles):
        self.logsDirectory = logsDirectory
        if not os.path.exists(logsDirectory):
            try:
                os.mkdir(logsDirectory)
            except OSError:
                print("Creation of the directory {0} failed".format(logsDirectory))
            else:
                print("Successfully created the directory {0} ".format(logsDirectory))
        self.numberOfFiles = numberOfFiles
        self.words = ('excel','gui','flash','word','doc','world','wiki','ppt','ssh','udp')
        self.SetUpClass()
    def addlogline(self,line,extra):
        print(line,extra)
        self.log.AddLogLine(line+" "+extra)
    def SetUpClass(self):
        self.okFiles = int(self.numberOfFiles / 2)
        # cls.dirtyFiles = cls.numberOfFiles / 2
        if not os.path.exists(self.logsDirectory):
            os.makedirs(self.logsDirectory)
    def GenearteFiles(self):
        ###
        # Log in to google web page and serach words from the list in self.words
        # and add to clean & dirty files that are saved in directory /dirty & /clean
        # ###
        try:
            gen = GenerateDirtyFileWithSelenium()
            dir_d = '{0}/{1}'.format(self.logsDirector,'dirty')
            if not os.path.exists(dir_d):
                os.makedirs(dir_d)
            dir_c = '{0}/{1}'.format(self.logsDirector, 'clean')
            if not os.path.exists(dir_c):
                os.makedirs(dir_c)
            os.chdir(dir_c)
            cwd = os.getcwd()
            len_w = len(self.words)
            eturate = (int)(self.okFiles / len_w)
            count = 0;
            for i in range(len_w):
                if count == self.numberOfFiles:
                    break
                value = randint(0, len_w)
                string = gen.searchGivenWord(self.words[value])
                for j in  range(eturate+1):
                    r = randint(i * 100, i * 10000000)
                    name_d = "{0}/DirtylogFile{1}{2}.dirty".format(dir_d, value, r)
                    r = randint(i * 200, i * 10000000)
                    name_l = "{0}/LogFile{1}{2}.clean".format(dir_c, value, r)
                    if not os.path.exists(name_d):
                        with open(name_d, "w", encoding="utf-8") as f:
                            f.write(string)
                            f.close()
                        count += 1
                    if not os.path.exists(name_l):
                        with open(name_l, "w", encoding="utf-8") as f:
                            f.write(string)
                            f.close()
                        count += 1
                    if count == self.numberOfFiles:
                        break
            gen.tearDownClass()
        except Exception as ex:
            template = "In GenerateDiertyFile Method GenearteFiles - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.addlogline(message)

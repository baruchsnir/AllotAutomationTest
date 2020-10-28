import os
import time
import multiprocessing
# from multiprocessing import Process, Lock
from threading import Thread,Lock
import os, sys, unittest, argparse, collections, copy, re, subprocess, importlib, pkgutil, json, datetime, glob, time
from .GenerateTestFiles import GenerateTestFiles
from .ManagDirectories import ManageDirectories
class ManagProccess:
    ###
    # Class that manage the process to run the application that we test and collect the stdout from the application
    # ###
    def __init__(self,logsDirectory,watchDirectory,applicationName,totalFilesGenerate,generatTests,log):
        self.log = log
        self.mutex = Lock()
        self.mutex1 = Lock()
        self.applicationStdOut = []
        self.logsDirectory = logsDirectory
        self.watchDirectory = watchDirectory
        self.applicationName = applicationName
        self.totalFilesGenerate = totalFilesGenerate
        wd = watchDirectory
        self.cmdToRunWatchProccess = [applicationName, "-w",wd]
        self.cmdToRunHelpProccess = [applicationName, "-h", wd]
        self.cmdToRunGenerateFileProccess = [applicationName, '-g','{0}'.format(self.totalFilesGenerate), "-o", wd]
        self.generatTests = generatTests
        self.watchProccess = Thread(target=self.ReadApplicationStdOut)
        global stopthread
        stopthread = False
    def StartWatchingApplication(self):
        ###
        # We use thread to run the application so we build method to start it
        # ###
        stopthread = False
        self.watchProccess.start()
    def closeWatchingProccess(self):
        ###
        # Closs the thread at the end
        # ###
        self.mutex.acquire()
        try:
        # with self.mutex:
            stopthread = True
        finally:
            self.mutex.release()
        #We add this file to allow the Application recognize the file and get out from block
        name_d = "{0}/DirtylogFileStopFile.clean".format(self.watchDirectory)
        with open(name_d, "w", encoding="utf-8") as f:
            f.write("Stop The Thread\r\n")
            f.close()
        self.watchProccess.join()
        # print("watchProccess finished thread")
    def addlogline(self,line,extra='',toconsole=True):
        ###
        # Add Line to console & to log file
        # ###
        if toconsole == True:
            print(line,extra)
        self.log.AddLogLine(line+" "+extra)
    def addreportline(self,line):
        ###
        # Add Line to Test Reports
        # ###
        self.log.AddReportLine(line)
    def ReadApplicationStdOut(self,**kwargs):
        ###
        # Method that run tha application and collect the stdout
        # The application watch the diretory and the stdout is save in applicationStdOut array
        # ###
        string  = 'Running "{}"'.format(str(self.cmdToRunWatchProccess))
        # print(string)
        self.addlogline(string)
        try:
            stopthread = False
            SubprocessResult = collections.namedtuple("SubprocessResult", "stdout stderr returncode")
            expect = ['ADD', 'DIRTY','ERROR']
            process = subprocess.Popen(self.cmdToRunWatchProccess, stdin=kwargs.get("stdin", subprocess.PIPE), stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, **kwargs)
            run = True
            while run:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    self.mutex.acquire()
                    try:
                        line = str(output.strip())
                        self.applicationStdOut.append(line)
                        if stopthread == True or  'DirtylogFileStopFile.clean' in line:
                            # print("watchProccess finished by stopthread")
                            stopthread = True
                            run  = False
                    finally:
                        self.mutex.release()
                    self.addlogline(str(output.strip()),'',False)
                if not run:
                    return
                if os.path.exists("{0}/DirtylogFileStopFile.clean".format(self.watchDirectory)):
                    run = False
                    # print("Found Stop File")
                    return
                if run:
                    rc = process.poll()
                else:
                    return
            out, err = process.communicate()
            stdout = []
            stderr = []
            mix = []
            if len(out) == 0:
                while process.poll() is None:
                    line = process.stdout.readline()
                    if line != "":
                        stdout.append(line)
                        mix.append(line)
                        # print(line, end='')
                        self.addlogline(str(line),"",False)
                    line = process.stderr.readline()
                    if line != "":
                        stderr.append(line)
                        mix.append(line)
                        self.addlogline(str(line), '', True)
            else:
                out = out.decode(sys.stdin.encoding)
                err = err.decode(sys.stdin.encoding)
                stdout.append(out)
                mix.append(out)
                stderr.append(err)
                mix.append(err)
        except EnvironmentError as ex:
            template = "In ManagProccess Method ReadApplicationStdOut - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.addlogline(message)
            self.addlogline("unable to run",self.cmdToRunWatchProccess)


    def GenerateFilesByApplication(self,**kwargs):
        ###
        # Method thar run the application in mode of generation dirty & clean files
        # ###
        string = 'Running "{}"'.format(str(self.cmdToRunGenerateFileProccess))
        # print(string)
        self.addlogline(string)
        expect = ['ADD', 'DIRTY','ERROR']
        try:
            SubprocessResult = collections.namedtuple("SubprocessResult", "stdout stderr returncode")
            expect = ['ADD', 'DIRTY','ERROR']
            process = subprocess.Popen(self.cmdToRunGenerateFileProccess, stdin=kwargs.get("stdin", subprocess.PIPE), stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, **kwargs)
            stdout = []
            stderr = []
            mix = []
            while process.poll() is None:
                line = process.stdout.readline()
                if line != "":
                    stdout.append(line)
                    mix.append(line)
                    self.addlogline(str(line),'',False)

                line = process.stderr.readline()
                if line != "":
                    stderr.append(line)
                    mix.append(line)
                    self.addlogline(str(line),'',True)


        except EnvironmentError as ex:
            template = "In ManagProccess Method GenerateFilesByApplication - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            self.addlogline(message)
            self.addlogline("unable to run",self.cmdToRunGenerateFileProccess)
    def GetStdOutArray(self):
        ###
        # Mathod to collect the applicationStdOut array and return it
        # We use the mutex to lock the array so the method ReadApplicationStdOut will be in hold
        # ###
        array = []
        self.mutex.acquire()
        try:
        # with self.mutex:
            array = self.applicationStdOut
        finally:
            self.mutex.release()
        # print('applicationStdOut------------------',array)
        # print('applicationStdOut------------------')
        return array
    def CleardOutArray(self):
        ###
        # Clear the applicationStdOut array,
        # We use the mutex to lock the array so the method ReadApplicationStdOut will be in hold
        # ##
        self.mutex.acquire()
        try:
            self.applicationStdOut.clear()
        finally:
            self.mutex.release()

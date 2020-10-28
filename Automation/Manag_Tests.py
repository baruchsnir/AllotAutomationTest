from .ManagDirectories import ManageDirectories
from .ManagProccess import ManagProccess
from .GenerateTestFiles import GenerateTestFiles
from .Log import Log
from datetime import datetime
import time
import allure

class Manag_Tests:
    ###
    # Class tha manage the tests
    # ###
    def __init__(self,logsDirectory,watchDirectory,applicationName):
        ###
        # Start the Test and build log directory , add the header of report file
        # ###
        self.logsDirectory = logsDirectory
        self.watchDirectory = watchDirectory
        self.applicationName = applicationName
        self.totalFilesGenerate = 100
        self.log = Log(logsDirectory)
        self.managedir = ManageDirectories(watchDirectory,self.log)
        self.generatTests = GenerateTestFiles(watchDirectory, self.totalFilesGenerate,self.log);
        self.mngproccess = ManagProccess(logsDirectory,watchDirectory,applicationName,self.totalFilesGenerate,self.generatTests,self.log)
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        tmp = str(applicationName)

        tmp = tmp.rsplit("/",1)[1]
        self.log.AddReportLine("=========================================================")
        self.log.AddReportLine("Test Application : "+tmp)
        self.log.AddReportLine("Date             :  "+date_time)
        self.log.AddReportLine("=========================================================")

    def addlogline(self,line,extra='',toconsole=True):
        ###
        # Add Line to console & to log file
        # ###
        if toconsole == True:
            print(line,extra)
        self.log.AddLogLine(line+" "+extra)
    def addreportline(self,line):
        ###
        # Add Line to report file
        # ###
        self.log.AddReportLine(line)
    @allure.severity(allure.severity_level.NORMAL)
    def test_GenerateFiles(self):
        ###
        # The first test that generat the Clean & Dirty files
        # ##
        result = True
        self.addreportline("1. Test Files Generating Process")
        self.addlogline(" *** Start Test Files Generating Process ***",'',True)
        self.managedir.clearFilesDirectory()
        self.mngproccess.GenerateFilesByApplication()
        if self.managedir.TestExistFiles(self.totalFilesGenerate):
            self.addreportline("1.1 PASS Generate Files")
            self.addlogline("Pass Generate Files - {0} in Directory {1}".format(self.totalFilesGenerate,self.watchDirectory),'',True)
        else:
            result = False
            self.addreportline("1.1 FAIL Generate Files")
            self.addlogline("Fail Generate Files", self.totalFilesGenerate)
            allure.attach('Generat Clean & Dirty Files', "Fail Generate Files")
            # assert result == False, "Fail Generate Files"
        self.addlogline(" *** End Test ***", '', True)
        return result
    @allure.severity(allure.severity_level.NORMAL)
    def test_WatchApplication(self):
        ###
        # Second test that copy all files that generate in test 1 and look on the test application screen
        # and collect the data
        # ###
        self.addreportline("2. Test Application in Watch Proccess")
        self.addlogline(" *** Start Test Application in Watch Proccess ***")
        # We clear the watch directory from all files
        self.managedir.clearWatchDirectory()
        self.mngproccess.StartWatchingApplication();
        # copy all files from test 1 to watch directory
        cleanFiles,dirtyFiles = self.generatTests.CopyFilesToWatchDirectory()
        self.addlogline("Sleep 120 Seconds for Application to test all files")
        # We wait more then 2 minutes to allow application to read the data
        # There is a problem with the application that after several files it stop reading the files data
        # also there is a problem in the speed of copy the files,if you copy the files in zero time
        # the application is not recognize most of the files, so we move to next test to change some files and then
        # the application read the files,so for now i do not know how to test it.

        count = 0
        result = True
        while(True):
            currentsize = self.mngproccess.GetStdOutArray()
            time.sleep(10)
            count += 10
            nextsize = self.mngproccess.GetStdOutArray()
            if len(currentsize) == len(nextsize) or count > 300:
                break
        self.addlogline(" Start Copy Clean & Dirty Files to Watch Directory")
        passtest,results = self.TestCopyFiles(self.mngproccess.GetStdOutArray(),cleanFiles,dirtyFiles)
        if passtest:
            self.addreportline("2.1 PASS Copy Clean & Dirty Files")
            self.addlogline("Pass Copy Clean & Dirty Files")
        else:
            result = False
            self.addreportline("2.1 FAIL Copy Clean & Dirty Files")
            self.addlogline("Fail Copy Clean & Dirty Files")
            count = 1
            for i in results:
                self.addreportline(" 2.1.{0} {1}".format(count,i))
                count += 1
        return result

    @allure.severity(allure.severity_level.NORMAL)
    def test_EditCleanFiles(self):
        ###
        # Second test that copy all files that generate in test 1 and look on the test application screen
        # and collect the data
        # ###
        num = 10
        self.addreportline("3. Test Edit Clean Files")
        self.addlogline(" Start Edit Clean {0} Files in Watch Directory".format(num))
        self.mngproccess.CleardOutArray()
        # Edit 10 clean files and look on the results from the application
        cahngedfiles = self.generatTests.EditSeveralCleanFile(num)
        time.sleep(10)
        passtest,results = self.TestChengesFiles(self.mngproccess.GetStdOutArray(),num,cahngedfiles)
        if  passtest:
            self.addreportline("3.1 PASS Change {0} Clean Files".format(num))
            self.addlogline("Pass Change {0} Clean Files".format(num))
        else:
            result = False
            self.addreportline("3.1 FAIL Change {0} Clean Files".format(num))
            self.addlogline("Fail Change {0} Clean Files".format(num))
            count = 1
            for i in results:
                self.addreportline(" 3.1.{0} {1}".format(count, i))
                count += 1

        return result
    def end_of_test(self):
        self.mngproccess.closeWatchingProccess()
        self.addlogline(" *** End Test ***", '', True)
        now = datetime.now()  # current date and time
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        self.addreportline("*** End Test {0} ***".format(date_time))
        self.log.AddReportLine("=========================================================")
    def TestCopyFiles(self,applicationStdOut,cleanFiles,dirtyFiles):
        ###
        # Test the lines that were read after we copy all clean & dirty files to watch directory
        # The method count the results from lines and fail the test if there is wrong test or error
        # ###
        countClean = 0
        countDirty = 0
        passtest = True
        results = []
        countDirtyMarkAsClean = 0
        countCleanMarkAsDirty = 0
        countChangedMarkAsDirty = 0
        countEror = 0;
        countRemoved = 0
        countRemovedAsClean = 0
        for line in applicationStdOut:
            if "ERROR" in line:
                countEror += 1
            for f in cleanFiles:
                if f in line:
                    if "ADDED" in line:
                        countClean += 1
                    if "DIRTY" in line:
                        countCleanMarkAsDirty += 1
                    if "REMOVED" in line:
                        countRemovedAsClean += 1
                    # self.TestCleanLine(line)
            for f in dirtyFiles:
                if f in line:
                    if "ADDED" in line:
                        countDirty += 1
                    if "CLEAN" in line:
                        countDirtyMarkAsClean += 1
                    if "CHANGED" in line:
                        countChangedMarkAsDirty += 1
                    if "REMOVED" in line:
                        countRemoved += 1
                    # self.TestCleanLine(line)
        string = ""
        if countClean + countDirty < self.totalFilesGenerate:
            passtest = False
            string = "Fail to read all {0} files".format(self.totalFilesGenerate)
            self.WriteResultsToLogs(string,"Copy Files To Watch Directory",True)
            results.append(string)

            self.addlogline("Fail to read all {0} files".format(self.totalFilesGenerate),'',True)
        if countEror > 0:
            passtest = False
            string = "Found {0} Errors".format(countEror)
            results.append(string)
            self.WriteResultsToLogs(string,"Copy Files To Watch Directory",True)
        if countCleanMarkAsDirty > 0:
            passtest = False
            string = "Found {0} Clean Files that were marked as DIRTY".format(countDirtyMarkAsClean)
            results.append(string)
            self.WriteResultsToLogs(string,"Copy Files To Watch Directory",True)
        if countRemovedAsClean > 0:
            passtest = False
            string ="Found {0} Clean Files that were marked as REMOVED".format(countDirtyMarkAsClean)
            results.append(string)
            self.WriteResultsToLogs(string, "Copy Files To Watch Directory", True)
        if countDirtyMarkAsClean > 0:
            passtest = False
            string = "Found {0} Dirty Files that were marked as CLEAN".format(countDirtyMarkAsClean)
            results.append(string)
            self.WriteResultsToLogs(string, "Copy Files To Watch Directory", True)
        if countChangedMarkAsDirty > 0:
            passtest = False
            string = "Found {0} Dirty Files that were marked as CHANGED".format(countChangedMarkAsDirty)
            results.append(string)
            self.WriteResultsToLogs(string, "Copy Files To Watch Directory", True)
        if countRemoved < countDirty:
            passtest = False
            string = "Only {0} Diray Files that were removed".format(countRemoved)
            results.append(string)
            self.WriteResultsToLogs(string, "Copy Files To Watch Directory", True)
        return passtest,results
    def WriteResultsToLogs(self,line,testname,toconsole=True):
        self.addlogline(line, '', toconsole)
        allure.attach(testname, line)
    def TestChengesFiles(self,applicationStdOut,num,cahngedfiles):
        ###
        # Test the lines that were read after we change some clean files to watch directory
        # The method count the results from lines and fail the test if there is wrong test or error
        # We only test the lines that include the name of the file if it was changed
        # There is a problem with tha application, it stuck to read the files, but after we chnage some files it is
        # continue to test other files that the application missed
        # ###
        countClean = 0
        passtest = True
        countCleanThatWasChanged = 0
        countDirtyMarkAsClean = 0
        countCleanMarkAsDirty = 0
        countChangedMarkAsDirty = 0
        countEror = 0;
        countRemoved = 0
        countRemovedAsClean = 0
        results = []
        # self.addlogline("-------------------------------", '', False)
        listofcahnges = []

        #We check only the clean files that we changed
        for line in applicationStdOut:
            find = False
            current = ''
            for file in cahngedfiles:
                if file in line:
                    find = True
                    current = file
                    break
            if find == False:
                continue
            # self.addlogline(line, '', False)
            if "ERROR" in line:
                countEror += 1
            if "CHANGED" in line:
                #There were a problem that file was marked as changed 2 times
                if not current in listofcahnges:
                    listofcahnges.append(current)
                    countCleanThatWasChanged += 1
            elif "ADDED" in line:
                countClean += 1
            elif "DIRTY" in line:
                countCleanMarkAsDirty += 1
            elif "REMOVED" in line:
                countRemovedAsClean += 1

        if countEror > 0:
            passtest = False
            string = "Found {0} Errors".format(countEror)
            results.append(string)
            self.WriteResultsToLogs(string, "Edit Clean Files", True)
        if countCleanThatWasChanged < num:
            passtest = False
            string = "Only {0} Clean Files that were CHANGED".format(countCleanThatWasChanged)
            results.append(string)
            self.WriteResultsToLogs(string, "Edit Clean Files", True)
        else:
            results.append("{0} Clean Files that were CHANGED".format(countCleanThatWasChanged))
            self.addlogline("{0} Clean Files that were CHANGED".format(countCleanThatWasChanged),'',True)
        if countClean > 0:
            passtest = False
            string = "Found {0} Changed Clean Files That ware Marked as ADD".format(countClean)
            results.append(string)
            self.WriteResultsToLogs(string, "Edit Clean Files", True)
        if countCleanMarkAsDirty > 0:
            passtest = False
            string = "Found {0} Clean Files that were marked as DIRTY".format(countCleanMarkAsDirty)
            results.append(string)
            self.WriteResultsToLogs(string, "Edit Clean Files", True)
        if countRemovedAsClean > 0:
            passtest = False
            string = "Found {0} Clean Files that were marked as REMOVED".format(countRemovedAsClean)
            results.append(string)
            self.WriteResultsToLogs(string, "Edit Clean Files", True)

        return passtest,results


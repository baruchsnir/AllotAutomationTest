import os
from datetime import datetime
global applicationStdOut
applicationStdOut = []
class Log:
    ###
    # Class the create log directory and allow to add data to log file and report file
    # ##
    def __init__(self, logsDirectory):
        ###
        # At the start we create the log directory,we seperate it to years and months
        # ###
        self.logsDirectory = logsDirectory
        MyMonthNames = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June",
                        7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
        now = datetime.now()  # current date and time
        if not os.path.exists(logsDirectory):
            try:
                os.mkdir(logsDirectory)
            except OSError:
                print("Creation of the directory {0} failed".format(logsDirectory))
            else:
                print("Successfully created the directory {0} ".format(logsDirectory))
        # date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        year = now.strftime("%Y")
        hh = now.strftime("%H")
        mmn = now.strftime("%M")
        ss = now.strftime("%S")
        dd = now.strftime("%d")
        mm = now.strftime("%m")
        month = MyMonthNames[int(mm)]
        if len(dd) == 1:
            dd = "0" + dd
        if len(mm) == 1:
            mm = "0" + mm
        if len(hh) == 1:
            hh = "0" + hh
        if len(mmn) == 1:
            mmn = "0" + mmn
        if len(ss) == 1:
            mmn = "0" + ss
        os.chdir(logsDirectory)
        dir = "{0}/{1}/{2}/{3}_{4}_{5}_{6}{7}/".format(logsDirectory, year, month, dd, mm, year, hh, mmn)
        if not os.path.exists(dir):
            try:
                if not os.path.exists(year):
                    os.mkdir(year)
                os.chdir(year)
                if not os.path.exists(month):
                    os.mkdir(month)
                os.chdir(month)
                tmp = "{3}_{4}_{5}_{6}{7}".format(logsDirectory, year, month, dd, mm, year, hh, mmn)
                if not os.path.exists(tmp):
                    os.mkdir(tmp)
            except OSError as ex:
                template = "In Log.py Method __init__ - An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print(message)
                print("Creation of the .log directory %s failed".format(dir))
        filename = "{0}/{1}_{2}_{3}_{4}{5}.log".format(dir, dd, mm, year, hh, mmn)
        if not os.path.exists(filename):
            with open(filename, "w+", encoding="utf-8") as f:
                f.write('')
                f.close()
        self.Logfilename = filename
        self.testreportfilename = "{0}/TestReport.txt".format(dir)
        if not os.path.exists(self.testreportfilename):
            with open(self.testreportfilename, "w+", encoding="utf-8") as f:
                f.write('')
                f.close()
    def AddLogLine(self,line):
        ###
        # Add line to log file
        # ###
        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S ")

        temp = date_time + str(line)+"\r";
        with open(self.Logfilename, "a", encoding="utf-8") as f:
            f.write(temp)
            f.close()
    def AddReportLine(self,line):
        ###
        # Add line to Report file
        # ###
        temp = str(line)+"\r\n";
        with open(self.testreportfilename, "a", encoding="utf-8") as f:
            f.write(temp)
            f.close()
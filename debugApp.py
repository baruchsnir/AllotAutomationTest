import sys, getopt
from Automation.Manag_Tests import  Manag_Tests
import allure
import sys
import os
class debugApp:
    def __init__(self):
        ###
        # setUpClass method that pars the arg that we got from command line
        # If there are no args it will take the defaults values
        # ###
        print("Configuration")
        with open('configuration.txt', 'r') as in_file:
            my_list = in_file.read().split('\n')
        argv = my_list
        if argv == None or len(argv) == 0:
            logsdirectory = "C:/Baruch/Alot/WorkSpace1/Reporting/Logs"
            watchdirectory = "C:/Baruch/Alot/WorkSpace1/WatchDirectory"
            applicationname = "C:/Baruch/Alot/Automation exercise/dist/node12-win-x64/index-win.exe"
        else:
            watchdirectory = 'C:/Baruch/Alot/WorkSpace1/WatchDirectory'
            applicationname = "index-win.exe"
            logsnirectory = 'C:/Baruch/Alot/WorkSpace1/Reporting/Logs'
            try:
                opts, args = getopt.getopt(argv, "a:h:w:l:",
                                           ["--ApplicationName", "--help", "--watch", "--logsDirectory"])
            except getopt.GetoptError:
                print('In order to Automation Test you have to give -a For application Name -w For Logs Folder.\n')
                print('Examples:\n')
                print(
                    '•   Start Running a Application - <run application> -a "index-win.exe" -w c:/Baruch/Alot/Automation exercise/test_files -l c:/Baruch/Alot/Automation exercise/Logs\'\n')
                print('\n\n')
                print('Options:\n')
                print('  -w, --watch <string>       Path to a folder to watch\n')
                print('  -a, --ApplicationName  Number of test files to generate, in the path given\n')
                print('  -l, --logsDirectory <string>      Path to output folder for logs files\n')
                print('  -h, --help                 output usage information\n')
            for opt, arg in opts:
                if opt == '-h' or opt == '-help':
                    print('In order to Automation Test you have to give -a For application Name -w For Logs Folder.\n')
                    print('Examples:\n')
                    print(
                        '•   Start Running a Application - <run application> -a "index-win.exe" -w c:/Baruch/Alot/Automation exercise/test_files -l c:/Baruch/Alot/Automation exercise/Logs\'\n')
                    print('\n\n')
                    print('Options:\n')
                    print('  -w, --watch <string>       Path to a folder to watch\n')
                    print('  -a, --ApplicationName  Number of test files to generate, in the path given\n')
                    print('  -l, --logsDirectory <string>      Path to output folder for logs files\n')
                    print('  -h, --help                 output usage information\n')
                    sys.exit()
                elif opt in ("-w", "--watch"):
                    watchdirectory = arg
                elif opt in ('-a', '--ApplicationName'):
                    applicationname = arg
                elif opt in ('-l', '--logsDirectory'):
                    logsdirectory = arg
        self.mngtests = Manag_Tests(logsdirectory, watchdirectory, applicationname)

    def test_application_generate_Files(self):
        ###
        # Test the function of application to generate files,we use this files later to copy themto watch directory
        # ###
        print("test_application_generate_Files")
        results = self.mngtests.test_GenerateFiles()
        # assert results == True

    def test_application_watch_directory(self):
        ####
        # Test the function of application to test clean & dirty files
        # ###
        results = self.mngtests.test_WatchApplication()
        # assert results == True

    def test_edit_clean_files(self):
        ####
        # Test the function of application to check clean files that were changed
        # ###
        results = self.mngtests.test_EditCleanFiles()
        # assert results == True


    def test_pytest_exit(self):
        self.mngtests.end_of_test()
        print("Test Completed")
# def main():
d = debugApp()
# d.test_setUpClass()
d.test_application_generate_Files()
d.test_application_watch_directory()
d.test_edit_clean_files()
d.test_pytest_exit()
# if __name__ == '__main__':
#     main()

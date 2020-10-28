import sys, getopt
from Automation.Manag_Tests import  Manag_Tests
import allure
import pytest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
@allure.severity(allure.severity_level.NORMAL)
class Test_Application:

    def pytest_report_header(config):
        return "project deps: Alot Test for application 'index-win.exe'"

    @pytest.fixture(scope="function")
    def test_setUpClass(self):
        ###
        # setUpClass method that pars the arg that we got from command line
        # If there are no args it will take the defaults values
        # ###
        with open('configuration.txt', 'r') as in_file:
            my_list = in_file.read().split('\n')
        argv = my_list
        if argv == None or len(argv) == 0:
            logsdirectory = "C:/Baruch/Alot/WorkSpace1/Reporting/Logs"
            watchdirectory = "C:/Baruch/Alot/WorkSpace1/WatchDirectory"
            applicationname = "c:/Baruch/Alot/WorkSpace/Application/index-win.exe"
        else:
            watchdirectory = 'C:/Baruch/Alot/WorkSpace1/WatchDirectory'
            applicationname = "index-win.exe"
            logsnirectory = 'C:/Baruch/Alot/WorkSpace1/Reporting/Logs'
            try:
                opts, args = getopt.getopt(argv,"a:h:w:l:",["--ApplicationName","--help","--watch","--logsDirectory"])
            except getopt.GetoptError:
                print('In order to Automation Test you have to give -a For application Name -w For Logs Folder.\n')
                print('Examples:\n')
                print('•   Start Running a Application - <run application> -a "index-win.exe" -w c:/Baruch/Alot/Automation exercise/test_files -l c:/Baruch/Alot/Automation exercise/Logs\'\n')
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
                    print('•   Start Running a Application - <run application> -a "index-win.exe" -w c:/Baruch/Alot/Automation exercise/test_files -l c:/Baruch/Alot/Automation exercise/Logs\'\n')
                    print('\n\n')
                    print('Options:\n')
                    print('  -w, --watch <string>       Path to a folder to watch\n')
                    print('  -a, --ApplicationName  Number of test files to generate, in the path given\n')
                    print('  -l, --logsDirectory <string>      Path to output folder for logs files\n')
                    print('  -h, --help                 output usage information\n')
                    sys.exit()
                elif opt in ("-w", "--watch"):
                    watchdirectory = arg
                elif opt in ('-a','--ApplicationName'):
                    applicationname = arg
                elif opt in ('-l','--logsDirectory'):
                     logsdirectory = arg
        global mngtests
        mngtests = Manag_Tests(logsdirectory, watchdirectory, applicationname)
        tmp = str(applicationname)

        tmp = tmp.rsplit("/",1)[1]
        allure.title('Test Application  {0}'.format(tmp))
    @allure.severity(allure.severity_level.NORMAL)
    def test_application_generate_Files(self,test_setUpClass):
        ###
        # Test the function of application to generate files,we use this files later to copy themto watch directory
        # ###
        print("test_application_generate_Files")
        results = mngtests.test_GenerateFiles()
        assert results == True

    @allure.severity(allure.severity_level.CRITICAL)
    def test_application_watch_directory(self):
        ####
        # Test the function of application to test clean & dirty files
        # ###
        results = mngtests.test_WatchApplication()
        if not results:
            assert False

    @allure.severity(allure.severity_level.CRITICAL)
    def test_edit_clean_files(self):
        ####
        # Test the function of application to check clean files that were changed
        # ###
        results = mngtests.test_EditCleanFiles()
        mngtests.end_of_test()
        if not results:
            assert False


    # @classmethod
    # @pytest.fixture(scope="class")
    # def test_pytest_exit(self):
    #     mngtests.end_of_test()
    #     print("Test Completed")

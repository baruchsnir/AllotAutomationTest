Allot Automation Test Project

This is a test project by allot for job QA Automation Engineer

There is an application index-win.exe that we need to test.

The application have 2 commands line
1. Generating clean & Dirty file
2. Watch the given directory and look on the files

    Application output is to console (STDOUT) and will follow this format 'TIME::!ACTION!::PATH'.
    Possible actions are [ADDED,CHANGED,DIRTY,REMOVED,CLEAN,ERROR]:
    •   ADDED   – new file added to the watched folder
    •   CHANGED – an existing file was changed in the watched folder
    •   DIRTY   – Application identified a file as dirty
    •   CLEAN   – Application identified a file as clean
    •   REMOVED – Application deleted the dirty file
    •   ERROR   - Application failed to process a file
    In order to generate test files you can use the -g [number] to create 50% dirty and 50% clean files.
    Examples:
    •   Generate files command - <run application> -g 1000 -o '/Baruch/Alot/Automation exercise/test_files'
    •   Start watching a folder - <run application> -w '/some_path/watched_folder'
	
i build 2 application 
1.AllotAutomationexercise.py - it is doing the same scenarios but it is not generating problems.
2.Test_Application.py - the application run the index-win.exe and collect the sdtout from it and analyes it.

there are 2 files that have to be edit according the place that this source will be locat


There is configuration file to place the directories according the workspace locate in the new PC
1. configuration.txt
-a
c:/Baruch/Alot/WorkSpace/Application/index-win.exe   -- location of application
-w
C:/Baruch/Alot/WorkSpace/WatchDirectory     -- location of the directory of watch files
-l
C:/Baruch/Alot/WorkSpace/Reporting/Logs     -- the location of reports 
2. Run.bat
Edit the run.bat according of new locations.
pytest -s -v --alluredir="C:/Baruch/Alot/WorkSpace/Reporting/Allure" --verbose --capture=no
allure serve C:/Baruch/Alot/WorkSpace/Reporting/Allure

To run the file you need to open pycharm and run it from the terminal

environment
----------------
Pycharm
Selenium
Pytest
Allure-pytest







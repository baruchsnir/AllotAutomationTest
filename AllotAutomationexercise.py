# This is the application you are require to test.
#     The application is watching changes to a specified folder and look for dirty files to delete.
#     The application identifies a dirty file by it's file extension '.dirty'.
#     Application output is to console (STDOUT) and will follow this format 'TIME::!ACTION!::PATH'.
#     Possible actions are [ADDED,CHANGED,DIRTY,REMOVED,CLEAN,ERROR]:
#     •   ADDED   – new file added to the watched folder
#     •   CHANGED – an existing file was changed in the watched folder
#     •   DIRTY   – Application identified a file as dirty
#     •   CLEAN   – Application identified a file as clean
#     •   REMOVED – Application deleted the dirty file
#     •   ERROR   - Application failed to process a file
#     In order to generate test files you can use the -g [number] to create 50% dirty and 50% clean files.
#     Examples:
#     •   Generate files command - <run application> -g 1000 -o '/Baruch/Alot/Automation exercise/test_files'
#     •   Start watching a folder - <run application> -w '/some_path/watched_folder'
#
# Options:
#   -w, --watch <string>       Path to a folder to watch
#   -g, --generate-data <int>  Number of test files to generate, in the path given
#   -o, --output <string>      Path to output folder for generated files
#   -h, --help                 output usage information
import sys, getopt
from GenerateFiles.GenerateDiertyFile import GenerateDiertyFile
from WatchFiles.ManageWatchDirestory import ManageWatchDirestory

def main(argv):
    ###
    # This is an application to generate clean & dirty files and watch changes in wartch directory
    # ###
    test_files_folder = ''
    test_files_deaufalt = 'C:/Baruch/Alot/WorkSpace1/WatchDirectory'
    watched_folder = ''
    watched_folder_deaufalt = test_files_deaufalt
    number_of_files = 0
    totaltime = 7500
    periodtime = 10
    try:
        opts, args = getopt.getopt(argv,"g:h:o:p:t:w:",["--generate-data","--help","--output","--PeriodTime","--TotalTime","--watch"])
    except getopt.GetoptError:
        print('In order to generate test files you can use the -g [number] to create 50% dirty and 50% clean files.\n')
        print('Examples:\n')
        print('•   Generate files command - <run application> -g 1000 -o \'c:/Baruch/Alot/Automation exercise/test_files\'\n')
        print('•   Start watching a folder - <run application> -w c:/Baruch/Alot/Automation exercise/test_files -t 100 -p 5\'\n')
        print('\n\n')
        print('Options:\n')
        print('  -w, --watch <string>       Path to a folder to watch\n')
        print('  -g, --generate-data <int>  Number of test files to generate, in the path given\n')
        print('  -o, --output <string>      Path to output folder for generated files\n')
        print('  -h, --help                 output usage information\n')
        print('  -t, --TotalTime            Total Time to watch directory in minutes\n')
        print('  -p, --PeriodTime           Period Time to watch directory in minutes,there are several cycles to watch files\n')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h' or opt == '-help':
            print('In order to generate test files you can use the -g [number] to create 50% dirty and 50% clean files.\n')
            print('Examples:\n')
            print('•   Generate files command - <run application> -g 1000 -o \'c:/Baruch/Alot/Automation exercise/test_files\'\n')
            print('•   Start watching a folder - <run application> -w c:/Baruch/Alot/Automation exercise/test_files -t 100 -p 5\'\n')
            print('\n\n')
            print('Options:\n')
            print('  -w, --watch <string>       Path to a folder to watch\n')
            print('  -g, --generate-data <int>  Number of test files to generate, in the path given\n')
            print('  -o, --output <string>      Path to output folder for generated files\n')
            print('  -h, --help                 output usage information')
            print('  -t, --TotalTime            Total Time to watch directory in minutes\n')
            print('  -p, --PeriodTime           Period Time to watch directory in minutes,there are several cycles to watch files\n')
            sys.exit()
        elif opt in ("-w", "--watch"):
            watched_folder = arg
            print('Start watch files in folder ', watched_folder)
        elif opt in ('-o','--output'):
            test_files_folder = arg
            print('Generate 50% dirty and 50% clean files in Folder ', test_files_folder)
        elif opt in ('-g','--generate-data'):
             number_of_files = int(arg)
             print('Generate total files ',number_of_files)
        elif opt in ('-t','--TotalTime'):
             totaltime = int(arg)
        elif opt in ('-p','--PeriodTime'):
             periodtime = int(arg)

    if number_of_files > 0:
        if test_files_folder == '':
            test_files_folder = test_files_deaufalt
        genfiles = GenerateDiertyFile(test_files_folder,number_of_files)
        genfiles.GenearteFiles();
    else:
        if watched_folder == '':
            watched_folder = watched_folder_deaufalt
        managedir = ManageWatchDirestory(watched_folder);
        managedir.WatchDirectory(totaltime,periodtime)
if __name__ == "__main__":
   main(sys.argv[1:])\
   # //        -g 100 -o 'c/Baruch/Alot/Automation exercise/test_files'
   #  -w 'c/Baruch/Alot/Automation exercise/test_files' -t 100 -p 5
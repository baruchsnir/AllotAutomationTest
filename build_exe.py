from distutils.core import setup
import py2exe

setup(
    console=['AllotAutomationexercise.py']   # the main py file
    # options={
    #         "py2exe":{
    #                 "packages": ["os", "linecache"],
    #                 "skip_archive": True, # tell script to not create a library folder
    #                 "unbuffered": True,
    #                 "optimize": 2
    #         }
    # }
)

#to run from command line 'c:\Python\Python38\python.exe  build_exe.py py2exe'


#c:\Python\Python38\python.exe AllotAutomationexercise.py

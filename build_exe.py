from distutils.core import setup
import py2exe
from selenium import webdriver
import allure
import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

setup(console=['AllotAutomationexercise.py'])

#to run from command line 'c:\Python\Python38\python.exe  build_exe.py py2exe'


#c:\Python\Python38\python.exe AllotAutomationexercise.py

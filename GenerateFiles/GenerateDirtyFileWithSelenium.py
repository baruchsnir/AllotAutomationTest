from selenium import webdriver
import allure
import pytest
# from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.options import Options
# # from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import time, re
import psutil
from bs4 import BeautifulSoup
...
# GenerateDirtyFileWithSelenium will automatically override this web driver
# Will Search in Google in https://google.com and will copy Page InnerHtml and put it in a given name file
# cls.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
...
class GenerateDirtyFileWithSelenium():
    ###
    # Open google.com and send word to search text box
    # ###
    def __init__(self):
        self.base_url = "https://www.google.com/"
        self.setUpClass()

    def setUpClass(self):
        ##
        # Set Up class to open Crome Driver and navigate to url
        # ###
        PROCNAME = "chromedriver.exe"
        for proc in psutil.process_iter():
            # check whether the process name matches
            if proc.name() == PROCNAME:
                proc.kill()
        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        time.sleep(1)
    def searchGivenWord(self,word):
        ###
        # Send word to search input and return string that include all the web elemnts by class name g
        # ###
        try:
            self.driver.find_element_by_name("q").clear()
            self.driver.find_element_by_name("q").send_keys(word + Keys.RETURN)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            string = ''
            gis = soup.find_all(class_="g")
            for g in gis:
                string += str(g.get_text())
            return string
        except Exception as ex:
            template = "In GenerateDirtyFileWithSelenium Method SearchGivenWord - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


    def is_Element_Present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e:
            return False
        return True

    def is_Alert_Present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e:
            return False
        return True

    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally:
            self.accept_next_alert = True
    def tearDownClass(self):
        ###
        # Close the chrom browser
        # ###
        try:
            self.driver.close()
            self.driver.quit()
            print("Test Completed")
        except Exception as ex:
            template = "In GenerateDirtyFileWithSelenium Method tearDownClass - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)
        try:
            self.driver.close()
        except Exception as ex:
            template = "In GenerateDirtyFileWithSelenium Method tearDown - An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)



import pytest
import os
import allure

from appium import webdriver
from selenium.common.exceptions import NoSuchElementException


class Test:

    GRAMS_BTN_XPATH = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' \
                      '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeTabBar[1]/XCUIElementTypeButton[2]'
    CREATE_GRAM_BTN_XPATH = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' \
                            '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther[1]' \
                            '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeButton[1]'
    CHOOSE_TRACK_TITLE_XPATH = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' \
                               '/XCUIElementTypeNavigationBar[1]/XCUIElementTypeStaticText[1]'
    FAVORITES_TAB_XPATH = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]' \
                          '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' \
                          '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeSegmentedControl[1]/XCUIElementTypeButton[1]'
    RECENT_TAB_XPATH = '//XCUIElementTypeApplication[1]/XCUIElementTypeWindow[1]/XCUIElementTypeOther[1]' \
                       '/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]/XCUIElementTypeOther[1]' \
                       '/XCUIElementTypeOther[1]/XCUIElementTypeSegmentedControl[1]/XCUIElementTypeButton[2]'

    @classmethod
    def setup(cls):
        #app = os.path.abspath('./Coffee Ratio/build/Debug-iphonesimulator/Coffee Ratio.app')
        #app = os.path.abspath('./iOS-iPhone/MusicGram/Build/MusicGram.app')
        app = os.path.abspath('./iOS-iPhone/MusicGram/Build/MusicGram.ipa')
        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'iOS',
                'platformVersion': '9.3.2',
                #'deviceName': "iPhone Simulator",
                #'deviceName': "iPhone",
                #'deviceName': "iPhone 7 plus",
                'deviceName': "Provectus iPhone 6S",
                #'udid': "87bfaac4f3292e2c309ac65005d536e498763f82",
                'udid': "4a229109c6e0979665efc7f934fb743aaefb37a3",
                "noReset": "false",
                "automationName": "xcuitest",
                "appiumVersion": "1.6.1-beta"
                #           'deviceName': 'iPhone 6'
            })

        cls.driver.implicitly_wait(300)
        #cls.driver.switch_to.alert.accept()

    @allure.feature('Create Gram')
    @allure.story('Test Choose Track')
    def test_open_choose_track(cls):
        cls.create_new_gram(cls)
        cls.allow_access_to_library(cls)
        cls.check_choose_track_screen(cls)

    def is_element_present(self, cls, element_xpath):
        try:
            cls.driver.find_element_by_xpath(element_xpath)
            return True
        except NoSuchElementException:
            return False

    def get_alert(self, cls):
        try:
            return cls.driver.switch_to_alert()            
        except NoAlertPresentException:
            return None

    @allure.step("Create new gram")
    def create_new_gram(self, cls):
        cls.driver.find_element_by_xpath(cls.GRAMS_BTN_XPATH).click()
        cls.driver.find_element_by_xpath(cls.CREATE_GRAM_BTN_XPATH).click()

    @allure.step("Check alert and allow access to the library")
    def allow_access_to_library(self, cls):
        alert = cls.get_alert(cls)
        assert alert is not None
        
        screen = cls.driver.get_screenshot_as_png()
        allure.attach('Alert', screen, allure.attach_type.PNG)
        
        alert.accept()

    @allure.step("Check Choose Track screen")
    def check_choose_track_screen(self, cls):
        assert cls.driver.find_element_by_xpath(cls.CHOOSE_TRACK_TITLE_XPATH).text == "CHOOSE TRACK"
        assert cls.is_element_present(cls, cls.FAVORITES_TAB_XPATH)
        assert cls.is_element_present(cls, cls.RECENT_TAB_XPATH)

        screen = cls.driver.get_screenshot_as_png()
        allure.attach('Choose track screen', screen, allure.attach_type.PNG)


    # @allure.step("Checking TBSP")
    # def check_tbsp(cls):
    #     cls.driver.find_element_by_xpath(cls.TBSP).click()
    #     assert cls.driver.find_element_by_xpath(cls.result).get_attribute("value") == "0.375"
    #     screen = cls.driver.get_screenshot_as_png()
    #     allure.attach('TBSP screen', screen, allure.attach_type.PNG)
    #
    # @allure.step("Checking Grams")
    # def check_gram(cls):
    #     cls.driver.find_element_by_xpath(cls.Grams).click()
    #     assert cls.driver.find_element_by_xpath(cls.result).get_attribute("value") == "18.5"
    #
    #     screen = cls.driver.get_screenshot_as_png()
    #     allure.attach('Grams sceen', screen, allure.attach_type.PNG)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

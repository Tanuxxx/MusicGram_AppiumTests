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
        app = os.path.abspath('./iOS-iPhone/MusicGram/Build/MusicGram.app')
        cls.driver = webdriver.Remote(
            command_executor='http://127.0.0.1:4723/wd/hub',
            desired_capabilities={
                'app': app,
                'platformName': 'iOS',
                'platformVersion': '10.0',
                'deviceName': "iPhone Simulator",
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
        cls.driver.find_element_by_xpath(cls.GRAMS_BTN_XPATH).click()
        cls.driver.find_element_by_xpath(cls.CREATE_GRAM_BTN_XPATH).click()
        
        cls.driver.switch_to.alert.accept()
        
        assert cls.driver.find_element_by_xpath(cls.CHOOSE_TRACK_TITLE_XPATH).text == "CHOOSE TRACK"
        assert cls.is_element_present(cls, cls.FAVORITES_TAB_XPATH)
        assert cls.is_element_present(cls, cls.RECENT_TAB_XPATH)

        screen = cls.driver.get_screenshot_as_png()
        allure.attach('GChoose track sceen', screen, allure.attach_type.PNG)


    def is_element_present(self, cls, element_xpath):
        try:
            cls.driver.find_element_by_xpath(element_xpath)
            return True
        except NoSuchElementException:
            return False


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

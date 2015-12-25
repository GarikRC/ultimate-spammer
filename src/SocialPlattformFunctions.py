# -*- coding: utf-8 -*-
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Exceptions
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException

__author__ = 'Qubasa'


def BuildBrowserProfile():
    try:
        profile = webdriver.FirefoxProfile('firefox-profile')
        driver = webdriver.Firefox(firefox_profile=profile)
    except IOError:
        driver = webdriver.Firefox()

    return driver


def WhatsAppSpammer(target, msg, quantity, browserSession=None):
    try:
        # Global settings
        if browserSession is None:
            browser = BuildBrowserProfile()
        else:
            browser = browserSession

        # Go to WhatsApp Web
        browser.get('https://web.whatsapp.com')
        WebDriverWait(browser, 180).until(EC.presence_of_element_located((By.CLASS_NAME, 'input')))

        # Search for target
        input_fields = browser.find_elements_by_class_name("input")
        search_contacts_field = input_fields[0]
        search_contacts_field.send_keys(target)

        # Select target in chat List
        spamming_target = browser.find_elements_by_xpath("//*[contains(text(), '%s')]" % target)
        spamming_target[0].click()
        time.sleep(1)

        # Text field to write message in
        input_fields = browser.find_elements_by_class_name("input")
        text_message_field = input_fields[1]

        for i in range(quantity):
            text_message_field.send_keys(msg)
            text_message_field.send_keys(Keys.RETURN)

        browser.close()

    except (WebDriverException, KeyboardInterrupt, IndexError) as error:
        browser.close()
        raise error


def FacebookSpammer(email, password, target, msg, quantity, browserSession=None):

    # Load Firefox profile
    if browserSession is None:
        browser = BuildBrowserProfile()
    else:
        browser = browserSession

    wait = WebDriverWait(browser, 10)

    try:
        # Go to Facebook
        browser.get('https://www.facebook.com/')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'inputtext')))

        # Log in to Facebook
        emailInput = browser.find_element_by_id("email")
        passwordInput = browser.find_element_by_id("pass")
        emailInput.send_keys(email)
        passwordInput.send_keys(password, Keys.ENTER)

        # Search for target and select chat
        try:
            wait.until(EC.presence_of_element_located((By.ID, 'u_0_1o')))
            time.sleep(1)
            searchInput = browser.find_element_by_id("u_0_1o")
        except TimeoutException:
            wait.until(EC.presence_of_element_located((By.ID, 'u_0_1p')))
            time.sleep(1)
            searchInput = browser.find_element_by_id("u_0_1p")

        searchInput.send_keys(target)
        time.sleep(2)
        searchInput.send_keys(Keys.ENTER)

        # Spam your Message
        for i in range(quantity):
            ActionChains(browser).send_keys(msg).perform()
            ActionChains(browser).send_keys(Keys.ENTER).perform()
        browser.close()

    except (WebDriverException, KeyboardInterrupt) as error:
        browser.close()
        raise error

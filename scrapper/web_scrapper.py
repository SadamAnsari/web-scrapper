import os
import logging
from explicit import ID
from explicit import waiter
from selenium.webdriver.common.by import By
from logger.logger import LOGGER_NAME
from selenium import webdriver
import time
import re

logger = logging.getLogger(LOGGER_NAME)

URL = "http://www.247singlewindowservices.com/"


class WebScrapper(object):
    def __init__(self, url, root_path):
        logger.info("Creating instance of {}".format(self.__class__.__name__))

        self.url = url
        self.browser = webdriver.Chrome(os.path.join(root_path, "chromedriver", "chromedriver.exe"))
        self.browser.set_window_size(1280, 1024)
        self.email_address = None
        self.phone_number = []

    def scrape_website(self):
        logger.info("Company URL::{}".format(self.url))
        # self.browser.get(self.url)
        self.scrape_contact_us()
        time.sleep(10)
        self.scrape_about_us()

    def scrape_contact_us(self):
        url = "{}/#contact".format(self.url)
        logger.info("Loading contact-us page. URL:: {}".format(url))
        self.browser.implicitly_wait(10)
        self.browser.get(url=url)
        content = self.browser.page_source
        email_regex = r'[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}'
        email_match = re.search(email_regex, content)
        if email_match:
            self.email_address = email_match.group(0)
            logger.info("Email Id: {}".format(self.email_address))

        phone_numbers = re.findall(r'[0-9]{4}[-]{1}[0-9]{7}', content)
        if phone_numbers:
            self.phone_number.extend(phone_numbers)
            logger.info("Phone numbers: {}".format(str(phone_numbers)))
        return

    def scrape_about_us(self):
        url = "{}/#about-us".format(self.url)
        logger.info("Loading about-us page. URL:: {}".format(url))
        self.browser.get(url=url)
        content = self.browser.page_source
        return




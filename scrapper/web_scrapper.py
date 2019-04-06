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

EMAIL_REGEX = r'[A-z0-9._%+-]+@[A-z0-9.-]+\.[A-z]{2,4}'
PHONE_REGEX = [r'[0-9]{4}[-]{1}[0-9]{7}', r'\([0-9]{3,4}\)\s*[0-9]{7}', r'\+91[0-9]{10}']


class WebScrapper(object):
    def __init__(self, name='', url='', company_contact=None, company_about=None, root_path=None):
        logger.info("Creating {0} instance of {1} company".format(self.__class__.__name__, name))
        self.company_name = name
        self.url = url
        self.contact = company_contact
        self.about = company_about
        self.browser = webdriver.Chrome(os.path.join(root_path, "chromedriver", "chromedriver.exe"))
        self.browser.set_window_size(1280, 1024)
        self.company_emails = []
        self.contact_numbers = []

    def get_info(self):
        logger.info("Company Name: {0}, Company URL: {1}".format(self.company_name, self.url))
        if not self.contact and not self.about:
            self.company_emails, self.contact_numbers = self.scrape_url()
            return True
        if self.contact:
            self.company_emails, self.contact_numbers = self.scrape_data()
            return True
        return None

    def scrape_url(self):
        self.browser.get(url=self.url)
        page_source = self.browser.page_source
        company_emails = self.get_email(content=page_source)
        contact_numbers = self.get_phone_numbers(content=page_source)
        logger.info("Company Name: {0}, Email: {1}, Phone Numbers: {2}".format(self.company_name, company_emails,
                                                                               contact_numbers))
        return company_emails, contact_numbers

    def scrape_data(self):
        url = "{0}/{1}".format(self.url, self.contact)
        logger.info("Loading contact-us page of company ({0}). URL:: {1}".format(self.company_name, url))
        self.browser.implicitly_wait(10)
        self.browser.get(url=url)
        page_source = self.browser.page_source
        company_emails = self.get_email(content=page_source)
        contact_numbers = self.get_phone_numbers(content=page_source)
        logger.info("Company Name: {0}, Email: {1}, Phone Numbers: {2}".format(self.company_name, company_emails,
                                                                               contact_numbers))
        return company_emails, contact_numbers

    def get_email(self, content):
        email_match = re.findall(EMAIL_REGEX, content)
        # print(re.findall(EMAIL_REGEX, content))
        return list(set(email_match))

    def get_phone_numbers(self, content):
        phone_numbers = []
        for regex in PHONE_REGEX:
            phone_numbers = re.findall(regex, content)
            if phone_numbers:
                # print(regex, print(re.findall(regex, content)))
                break
        return list(set(phone_numbers))

    # def scrape_about_us(self):
    #     url = "{}/#about-us".format(self.url)
    #     logger.info("Loading about-us page. URL:: {}".format(url))
    #     self.browser.get(url=url)
    #     content = self.browser.page_source
    #     return




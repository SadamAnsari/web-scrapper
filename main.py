import os
import logging
from logger.logger import setup_logging, LOGGER_NAME
from scrapper.web_scrapper import WebScrapper

logger = logging.getLogger(LOGGER_NAME)

root_path = os.path.dirname(os.path.abspath(__file__))


def main():
    print(root_path)
    setup_logging(logdir=os.path.join(root_path, "logs"), logfile="web_scrapper.log", scrnlog=True)
    instance = WebScrapper(url="http://www.247singlewindowservices.com/",
                           root_path=root_path)
    instance.scrape_website()
    company_email = instance.email_address
    company_phone = instance.phone_number
    print(company_email, "\t", company_phone)

if __name__ == '__main__':
    main()
import os
import json
import logging
from logger.logger import setup_logging, LOGGER_NAME
from scrapper.web_scrapper import WebScrapper
from utility.util import read_from_csv
logger = logging.getLogger(LOGGER_NAME)

root_path = os.path.dirname(os.path.abspath(__file__))


def main():
    print(root_path)
    setup_logging(logdir=os.path.join(root_path, "logs"), logfile="web_scrapper.log", scrnlog=True)
    company_list = read_from_csv(file_path=os.path.join(root_path, "misc" + os.sep + "details.csv"))
    company_detail = []
    for company in company_list:
        company_dict = {}
        company_name = company.get('name')
        company_contact = company.get('contact_page')
        company_about = company.get('about_page')
        company_url = company.get('url')
        # print(company_name, company_url, company_contact, company_about)
        scrapper = WebScrapper(name=company_name, url=company_url, company_contact=company_contact,
                               company_about=company_about, root_path=root_path)
        scrapper.get_info()
        company_dict['company'] = company_name
        if scrapper.company_emails:
            company_dict['email'] = scrapper.company_emails
        if scrapper.contact_numbers:
            company_dict['phone'] = scrapper.contact_numbers
        company_detail.append(company_dict)
        # break
    output_path = os.path.join(root_path, 'data' + os.sep + 'output.json')
    with open(output_path, 'w') as f:
        f.write(json.dumps(company_detail, indent=4))

if __name__ == '__main__':
    main()
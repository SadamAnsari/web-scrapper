
"""
    Utility Package
"""
import csv
import logging
from logger.logger import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def read_from_csv(file_path):
    try:
        csv_file = open(file_path, 'r')
        csv_reader = csv.reader(csv_file)
        header = next(csv_reader)
        results = []
        for row in csv_reader:
            results.append(dict(zip(header, row)))
        return results
    except IOError as e:
        logger.info("Could not read file: I/O error({0}): {1}".format(e.errno, e.strerror))
    except Exception as ex:
        logger.exception(ex)
        raise Exception("Error caught in read_from_csv function.")

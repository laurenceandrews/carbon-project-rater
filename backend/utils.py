import csv
import logging
import os

industry_types = {}

def load_industry_types():
    global industry_types
    filepath = os.path.join(os.path.dirname(__file__), 'data', 'Industry Types.csv')
    with open(filepath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        logging.debug(f"CSV Headers: {headers}")
        for row in reader:
            try:
                industry_types[row['Subpart Letter']] = row['Name of industry']
                logging.debug(f"Loaded industry type: {row['Subpart Letter']} -> {row['Name of industry']}")
            except KeyError as e:
                logging.error(f"KeyError: {e} - Row: {row}")
    logging.debug("Industry types loaded successfully.")
    logging.debug(f"All loaded industry types: {industry_types}")

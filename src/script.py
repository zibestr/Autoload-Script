import logging
import os
from datetime import datetime

import dotenv
import gspread
import psycopg2

from sql_scripts import select_data_script

dotenv.load_dotenv()
API_KEY = os.getenv('SERVICE_ACCOUNT_FILENAME')
URL = os.getenv('SHEET_URL')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
UPDATE_TIME = (0, 0)


def autoload():
    now_datetime = datetime.now()
    log_filename = (f'logs/{now_datetime.day}.{now_datetime.month}.'
                    f'{now_datetime.year} {now_datetime.hour}:'
                    f'{now_datetime.minute}:{now_datetime.second}.log')
    logging.basicConfig(level=logging.INFO,
                        filename=log_filename,
                        filemode='w',
                        format='%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger('autoloader')

    is_work = True
    logger.info('Running script')

    try:
        db_conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER,
                                   password=DB_PASSWORD, host=DB_HOST)
        logger.info('Connecting to database')
    except Exception as e:
        logger.exception(e)
        raise SystemExit

    api = gspread.service_account(
        filename=API_KEY
    )
    logger.info('Connecting to API')

    spread = api.open_by_url(
        URL
    )
    logger.info('Connecting to spreadsheet')

    worksheet = spread.get_worksheet(0)
    try:
        last_date = None
        while is_work:
            now_time = datetime.now()

            if (now_time.hour, now_time.minute) == (12, 43) \
               and last_date != (now_time.day, now_time.month):
                last_date = (now_time.day, now_time.month)

                logger.info('Start script')
                response = download_from_db(db_conn)
                logger.info('Load data from DB')
                logger.debug(f'Get data: {response}')

                response = format_response(response)
                upload_to_spreadsheet(worksheet, response)
                logger.info('Upload data to spreadsheet')

    except KeyboardInterrupt:
        is_work = False
        db_conn.close()
        logger.info('Close connection to database')
        logger.info('Script shutdown')

    except Exception as e:
        db_conn.close()
        logger.exception(e)


def download_from_db(connection) -> list:
    # TODO: edit download function and SQL script
    with connection.cursor() as cursor:
        cursor.execute(select_data_script)
        response = cursor.fetchall()
        return response


def format_response(response: list) -> list:
    # TODO: edit format function
    return [[row[1]] for row in response]


def upload_to_spreadsheet(worksheet: gspread.worksheet.Worksheet, data: list):
    # TODO: edit upload function
    len_worksheet = len(worksheet.get_all_values()[0])
    worksheet.update(data,
                     f'A{len_worksheet + 1}:A{len_worksheet + 1 + len(data)}')


if __name__ == '__main__':
    autoload()

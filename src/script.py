import logging
from datetime import datetime


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
        while is_work:
            pass
    except KeyboardInterrupt:
        is_work = False
        logger.info('Script shutdown')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    autoload()

import os
import logging
from datetime import datetime
from typing import Optional, List


CURRENCY = (
    'GBP', 'HKD', 'USD', 'CHF', 'SGD', 'PKR', 'SEK',
    'DKK', 'NOK', 'JPY', 'CAD', 'AUD', 'MYR', 'EUR',
    'RUB', 'MOP', 'THB', 'NZD', 'ZAR', 'KZT', 'KRW'
)


def get_logger(name: str,
               logfmt: str = '[%(asctime)s][%(name)s][%(filename)s][%(levelname)s]: %(message)s',
               datefmt: str = '%Y-%m-%d %H:%M:%S',
               level: str = 'DEBUG',
               filename: Optional[str] = None):
    # Create a custom logger
    logger = logging.getLogger(name)

    # Set the logging level and format for this logger
    logger.setLevel(getattr(logging, level, 'DEBUG'))

    # check filename
    if filename is not None:
        if not filename.endswith('.log'):
            filename += '.log'
        filename = 'logs/' + filename
        # check if the logs folder exists
        if not os.path.exists('logs'):
            filename = None
            print('The logs folder does not exist. The log will be output to the console.')

    # create handler
    if filename is not None:
        # Create a file handler to output log messages to a file
        handler = logging.FileHandler(filename)
        handler.setFormatter(logging.Formatter(logfmt, datefmt))
    else:
        # output log messages to console
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(logfmt, datefmt))
    logger.addHandler(handler)
    return logger


logger = get_logger('utils', filename='utils.log')


def find_files(path: str, ext: str = 'csv') -> List[str]:
    # check path exists
    if not os.path.exists(path):
        logger.error(f"The path does not exist: {path}")
        raise FileNotFoundError(f"The path does not exist: {path}")
    # check ext
    if not ext.startswith('.'):
        ext = '.' + ext
    # find files
    items = os.listdir(path)
    if not items:
        logger.warning(f"No files found in {path}")
        return []
    files = [item for item in items if os.path.isfile(os.path.join(path, item)) and item.endswith(ext)]
    if not files:
        logger.warning(f"No {ext} files found in {path}")
        return []
    return files


# Function to convert the string to a datetime object
def str_to_datetime(date_str):
    return datetime.strptime(date_str, '%Y_%m_%d-%H_%M_%S')


def get_latest_file(path: str, ext: str = 'csv') -> Optional[str]:
    files = find_files(path=path, ext=ext)
    if len(files) == 0:
        logger.error(f"No latest file found in {path}, because no {ext} files found.")
        return None
    else:
        # get the latest file
        files.sort(reverse=True, key=lambda x: str_to_datetime(os.path.basename(x).split('.')[0]))
        logger.info(f"Found latest file: {files[0]}")
        return os.path.join(path, files[0])


def get_outdated_files(path: str, ext: str = 'csv', days: int = 60) -> List[str]:
    files = find_files(path=path, ext=ext)
    if len(files) == 0:
        logger.error(f"No outdated files found in {path}, because no {ext} files found.")
        return []
    else:
        # get the latest file
        files.sort(reverse=True, key=lambda x: str_to_datetime(os.path.basename(x).split('.')[0]))
        latest_file = files[0]
        # get the datetime of the latest file
        latest_file_datetime = str_to_datetime(os.path.basename(latest_file).split('.')[0])
        # get the outdated files
        outdated_files = [os.path.join(path, file) for file in files if (latest_file_datetime - str_to_datetime(os.path.basename(file).split('.')[0])).days > days]
        if len(outdated_files) == 0:
            logger.info(f"No outdated files found in {path}.")
        else:
            logger.info(f"Found {len(outdated_files)} outdated files in {path}.")
        return outdated_files


if __name__ == '__main__':
    file = get_latest_file(path='../assets', ext='csv')
    print(file)

import os
import pandas as pd
from dotenv import load_dotenv
from pypushdeer import PushDeer
try:
    from .utils import get_logger
except ImportError:
    from utils import get_logger


logger = get_logger('Trigger', filename='trigger.log')
# load dotenv in the project root folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))
# initialize PushDeer
push_key = os.getenv('PUSH_DEER_TOKEN', None)
if push_key is None:
    logger.error('PUSH_DEER_TOKEN is not set.')
    pushdeer = None
else:
    pushdeer = PushDeer(pushkey=push_key)


"""
Requirements for the trigger functions:
1. The function name must start with "trigger_".
2. The function must accept a pandas.DataFrame object as the first and required positional argument.
3. The function must return a boolean value indicating whether the trigger is successfully executed.
4. Use `try` and `except` to catch any exceptions.
"""


def trigger_when_price_is_lower_than(
        df: pd.DataFrame,
        currency: str = 'EUR',
        threshold: float = 750.0,
        label_currency: str = '代号',
        label_exchsell: str = '现汇卖出价',
        debug: bool = False
) -> bool:
    """
    Trigger when the EUR exchange sell price is below the threshold.
    """
    # get params from environment variables
    currency = os.getenv('WATCHER_CURRENCY_CODE', currency).upper()
    threshold = float(os.getenv('WATCHER_PRICE_LOWER_THAN', threshold))
    label_currency = os.getenv('WATCHER_CUR_LABEL', label_currency)
    label_exchsell = os.getenv('WATCHER_PRICE_LABEL', label_exchsell)

    try:
        price = df[df[label_currency] == currency].iloc[0][label_exchsell]

        if debug:
            logger.debug(f"EUR exchange sell price: {price}")

        if price < threshold:
            if pushdeer is not None:
                pushdeer.send_text(f"Currency Watcher\nEUR exchange sell price is now at {price} "
                                   f"(threshold: {threshold}).")
            logger.info(f"EUR exchange sell price ({price}) is below threshold ({threshold}).")
    except Exception as e:
        logger.error(f"Failed to run <trigger_when_price_is_lower_than>: {e}")
        return False
    return True


if __name__ == '__main__':
    # test the trigger functions
    from parse import parse_csv
    trigger_when_price_is_lower_than(
        parse_csv(
            '../assets/2023_04_05-03_21_02.csv',
            debug=True
        ),
        debug=True
    )

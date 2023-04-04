import os
import pandas as pd
from typing import Optional
import trigger
try:
    from .fetch import fetch_html_content
    from .parse import parse_html, parse_csv
    from .utils import get_outdated_files, get_latest_file, get_logger, CURRENCY, \
        get_modules
except ImportError:
    from fetch import fetch_html_content
    from parse import parse_html, parse_csv
    from utils import get_outdated_files, get_latest_file, get_logger, CURRENCY, \
        get_modules


logger = get_logger('Index', filename='index.log')
triggers = get_modules(trigger, prefix='trigger_')


def pipeline(
        url: str,
        storage: Optional[str] = None,
        verbose: bool = False,
        debug: bool = False,
        clean: bool = False,
        use_triggers: bool = False
) -> Optional[pd.DataFrame]:
    # fetch html content
    if verbose:
        print(f"Fetching html content from: {url}")
    html_content = fetch_html_content(url=url)
    if html_content is None:
        _log('No html content to parse.', verbose=verbose, level='error')
        return

    # parse html content
    if verbose:
        print('Parsing html content.')
    df = parse_html(html_content, debug=debug)
    if df is None:
        _log('Failed to parse the html content.', verbose=verbose, level='error')
        return

    # use triggers
    if verbose:
        print('Activating triggers.')
    if use_triggers:
        for fn in triggers:
            try:
                st = fn(df)
            except Exception as e:
                _log(f"Uncaught error occurred in Trigger <{fn.__name__}>. "
                     f"It will be removed from future scheduled jobs. "
                     f"Restart the backend to re-enable it.",
                     verbose=verbose,
                     level='critical')
                triggers.remove(fn)
                continue

            # report results
            if st:
                _log(f"Trigger <{fn.__name__}> executed.", verbose=verbose)
            else:
                _log(f"Trigger <{fn.__name__}> failed.", verbose=verbose, level='error')

    # save to storage
    if verbose:
        print('Saving to storage.')
    if storage is not None:
        # check storage path exists
        if not os.path.exists(storage):
            _log(f"Storage path does not exist: {storage}", verbose=verbose, level='error')
            return df
        else:
            # make filename as datetime from df
            filename = os.path.join(storage, df['发布时间'].iloc[0].strftime('%Y_%m_%d-%H_%M_%S') + '.csv')
            # save to storage
            df.to_csv(filename, header=True, index=False)
            _log(f"Successfully saved to storage: {storage}", verbose=verbose)

    # clean storage if files are 60 days away from the latest file
    if verbose:
        print('Cleaning storage.')
    if clean:
        outdated_files = get_outdated_files(storage, ext='csv', days=60)
        if len(outdated_files) > 0:
            for file in outdated_files:
                try:
                    os.remove(file)
                    _log(f"Successfully removed file: {file}", verbose=verbose)
                except OSError:
                    _log(f"Failed to remove file: {file}", verbose=verbose, level='error')

    if verbose:
        print('Pipeline finished.')
    return df


def get_exchange_rate(
        url: str,
        currency: str = 'EUR',
        now: bool = True,
        storage: str = 'assets/',
        verbose: bool = False,
        debug: bool = False
) -> Optional[pd.DataFrame]:
    if verbose:
        print(f"Getting the exchange rate of {currency} from url: {url}")

    # run pipeline to get the currency exchange rate
    if not now:
        # get currency exchange rate from storage
        filename = get_latest_file(storage)
        if filename is None:
            logger.error(f'Failed to get the latest file in {storage}. Use pipeline to get the exchange rate.')
            df = pipeline(url=url, debug=debug)
        else:
            if verbose:
                print('Getting the exchange rate from storage.')
            df = parse_csv(filename, debug=debug)
    else:
        if verbose:
            print('Getting the exchange rate at present.')
        df = pipeline(url=url, debug=debug)

    if df is None:
        logger.error('Failed to get the exchange rate DataFrame.')
        return

    # validate currency
    currency = currency.upper()
    if currency in CURRENCY:
        # filter out the rows with '代号' == currency
        df = df[df['代号'] == currency]
    elif currency not in CURRENCY and currency != 'ALL':
        logger.error(f"Invalid currency: {currency}.")
        return

    if debug:
        logger.debug(f"Successfully got the exchange rate of {currency}:\n{df}")
    if verbose:
        print(f"Successfully got the exchange rate of {currency}:\n{df}")
    return df


def get_exchange_rate_bank_sell(*args, **kwargs):
    if 'currency' not in kwargs:
        print("Please specify the currency.")
        return
    df = get_exchange_rate(*args, **kwargs)
    print(f"{kwargs['currency']} 现汇卖出价: {df['现汇卖出价'].iloc[0]}")
    return


def get_exchange_rate_api(*args, **kwargs):
    df = get_exchange_rate(*args, **kwargs)

    if df is None:
        return {
            'status': 'error',
            'message': 'Failed to get the exchange rate.'
        }

    # create response
    exch_rate = [
        {
            'currency': cur,
            'name': name,
            'exch_buy': exch_buy,
            'exch_sell': exch_sell,
            'cash_buy': cash_buy,
            'cash_sell': cash_sell
        }
        for cur, name, exch_buy, cash_buy, exch_sell, cash_sell in
        zip(*df.drop('发布时间', axis=1).to_dict(orient='list').values())
    ]
    response = {
        'status': 'success',
        'data': exch_rate
    }

    return response


def _log(msg: str, verbose: bool = False, level: str = 'info'):
    if verbose:
        print(msg)
    if level.lower() == 'info':
        logger.info(msg)
    elif level.lower() == 'error':
        logger.error(msg)
    elif level.lower() == 'debug':
        logger.debug(msg)
    elif level.lower() == 'warning':
        logger.warning(msg)
    elif level.lower() == 'critical':
        logger.critical(msg)
    return


if __name__ == '__main__':
    print(get_exchange_rate(
        url="https://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx",
        storage='../assets/',
        now=False
    ))
    print(get_exchange_rate_api(
        url="https://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx",
        currency='EUR',
        storage='../assets/',
        now=False
    ))


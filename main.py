import argparse
from src import pipeline, get_exchange_rate, get_exchange_rate_bank_sell


URL = 'https://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx'


parser = argparse.ArgumentParser(description='Currency exchange rate bot.')
# mode 1: query the exchange rate at present/from storage
parser.add_argument('--currency', '-c', type=str, help='Query specific currency')
parser.add_argument('--now', '-n', action='store_true',
                    help='Use with --currency to query the current exchange rate at present.')
# mode 2: fetch the exchange rate from website and save to storage
parser.add_argument('--pipeline', '-p', action='store_true',
                    help='Run pipeline to fetch the exchange rate from website and save to storage.')
parser.add_argument('--storage', '-s', type=str, help='Specify the storage path.')
# common arguments
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode.')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.currency:
        df = get_exchange_rate_bank_sell(
            url=URL,
            currency=args.currency,
            now=args.now,
            verbose=args.verbose
        )
    if args.pipeline:
        df = pipeline(
            url=URL,
            storage=args.storage,
            verbose=args.verbose
        )

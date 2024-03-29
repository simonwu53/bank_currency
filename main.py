import argparse
import os
from src import pipeline, get_exchange_rate_bank_sell


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
parser.add_argument('--clean', action='store_true', help='Clean the storage files than is older than 60 day.')
parser.add_argument('--use-triggers', action='store_true', help='Enable triggers.')
# common arguments
parser.add_argument('--verbose', '-v', action='store_true', help='Verbose mode.')
parser.add_argument('--debug', action='store_true', help='print out debug info.')


if __name__ == '__main__':
    # check current working directory equals to the file directory
    cwd = os.getcwd()
    if cwd != os.path.dirname(os.path.abspath(__file__)):
        print('Please run this script from the root directory of the project. '
              f'Current working directory: {cwd}, '
              f'Project root directory: {os.path.dirname(os.path.abspath(__file__))}')
        exit(1)

    args = parser.parse_args()
    print(args)
    if args.currency:
        get_exchange_rate_bank_sell(
            url=URL,
            currency=args.currency,
            now=args.now,
            verbose=args.verbose,
            debug=args.debug
        )
        exit(0)
    if args.pipeline:
        print(pipeline(
            url=URL,
            storage=args.storage,
            verbose=args.verbose,
            debug=args.debug,
            clean=args.clean,
            use_triggers=args.use_triggers
        ))
        exit(0)
    print('No action specified. One must set either --currency or --pipeline flag. Use -h to see help.')

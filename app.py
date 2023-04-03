import os
from dotenv import load_dotenv
from waitress import serve
from flask import Flask, request, abort, url_for, redirect
from src import get_exchange_rate_api


load_dotenv()
app = Flask(__name__)
API_PREFIX = os.getenv('FLASK_API_URL_PREFIX', '/api')


@app.route(os.path.join(API_PREFIX, 'exchangerate'))
def eur_exch_sell_rate():
    # check request headers authorization
    auth = request.headers.get('Authorization', '')
    key = os.getenv('FLASK_API_AUTH_TOKEN')
    if not key:
        app.logger.error('FLASK_API_AUTH_TOKEN is not set.')
        return redirect(url_for('not_found'))
    if auth == '' or auth != key:
        app.logger.error('Invalid Authorization.')
        return redirect(url_for('not_found'))

    # get query parameters
    currency = request.args.get('currency', 'none')
    if currency == 'none':
        app.logger.error('No currency specified.')
        return redirect(url_for('not_found'))

    now = request.args.get('now', 'false')
    if now.lower() == 'true':
        now = True
    else:
        now = False

    # call api
    exch_rate = get_exchange_rate_api(
        url='https://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx',
        currency=currency,
        now=now,
        storage='assets/',
    )
    return exch_rate


@app.route('/not_found')
def not_found():
    abort(404)


@app.errorhandler(404)
def page_not_found(error):
    return "The page you access does not exist.", 404


if __name__ == '__main__':
    # Running on http://127.0.0.1:5000
    # app.run(debug=True)
    serve(app, host='127.0.0.1', port=5000)

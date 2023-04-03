import os
from dotenv import load_dotenv
from flask import Flask, request, abort, url_for, redirect
from src import get_exchange_rate_api


load_dotenv()
app = Flask(__name__)

@app.route('/api/v1/exchangerate')
def eur_exch_sell_rate():
    # check request headers authorization
    auth = request.headers.get('Authorization', '')
    key = os.getenv('FLASK_API_AUTH_TOKEN')
    if auth == '' or auth != 'Bearer ' + key:
        return redirect(url_for('not_found'))

    # get query parameters
    now = request.args.get('now', 'false')
    if now.lower() == 'true':
        now = True
    else:
        now = False
    currency = request.args.get('currency', 'ALL')

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
    app.run(debug=True)

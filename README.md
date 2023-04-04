# bank_currency
Get the currency exchange rate from ICBC via Flask API

## 1. Setup

0. create `.env` file at root dir as follows

```bash
# edit .env file
# Flask API Token (required)
FLASK_API_AUTH_TOKEN=your_token

# default API url prefix
FLASK_API_URL_PREFIX=/api
```

1. create virtual environment

```bash
# pip
python3 -m venv icbc
source icbc/bin/activate

# conda
conda create --name icbc python=3.10
conda activate icbc
```

2. install requirements as follows

```bash
# pip
pip install -r requirements.txt

# conda
conda install requests pandas flask beautifulsoup4 python-dotenv
conda install -c conda-forge waitress

# push notification
pip install pypushdeer
```

## 2. Run
### 2.1 Run API server

```bash
# run the flask server
flask run --port 5000

# run WSGI server
python app.py
```

### 2.2 Run periodic task (require conda env)
Run once:
```bash
bash exe/job.sh
```

Use crontab:
```bash
# edit crontab
crontab -e

# add the following line
# At minute 5 past every hour.
5 */1 * * * /bin/bash /path/to/exe/job.sh
```


## 3. Call API
The default host will run at localhost: `http://127.0.0.1:5000`

```bash
# api call for a specific currency
http://127.0.0.1:5000/api/exchangerate?currency=EUR&now=true

# api call for all currencies
http://127.0.0.1:5000/api/exchangerate?currency=all
```


## TODO:

| Bank | Exchange Rate |
| --- | --- |
| Bank of Communications | [Link](https://www.bankcomm.com/BankCommSite/zonghang/cn/whpj/foreignExchangeSearch_Cn.jsp)   |

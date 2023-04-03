# bank_currency
Get the currency exchange rate from ICBC via Flask API

## 1. Setup

0. create `.env` file at root dir as follows

```bash
# .env
FLASK_API_AUTH_TOKEN=your_token
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
conda install --file requirements.txt
```

## 2. Run
### 2.1 Run API server

```bash
# run the flask app
flask run --port 5000
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
5 */1 * * * bash /path/to/exe/job.sh
```


## 3. API



## TODO:

| Bank | Exchange Rate |
| --- | --- |
| Bank of Communications | [Link](https://www.bankcomm.com/BankCommSite/zonghang/cn/whpj/foreignExchangeSearch_Cn.jsp)   |

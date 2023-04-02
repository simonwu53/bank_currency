from bs4 import BeautifulSoup as bs
import pandas as pd
from typing import List, Optional
try:
    from .utils import get_logger
except ImportError:
    from utils import get_logger


logger = get_logger('parser', filename='parser.log')


def parse_html(html: str) -> Optional[pd.DataFrame]:
    # parse html
    soup = bs(html, 'lxml')

    # get table content
    col_types = [str, float, float, float, float, str]
    cols: List[str] = []
    data: List[dict] = []
    dtypes: dict = {}
    for i, row in enumerate(soup.html.body.form.div.table.tr.td.table.contents[2].contents[1].find_all('tr')):
        # columns: "币种", "现汇买入价", "现钞买入价", "现汇卖出价", "现钞卖出价", "发布时间"
        # dtype: str, float, float, float, float, str
        if i == 0:
            cols = [col.string for col in row.find_all('td')]
            if not cols:
                logger.error('Failed to parse the table header.')
                return None
            else:
                dtypes = dict(zip(cols, col_types))
        else:
            data.append(dict(zip(cols, [col.string for col in row.find_all('td')])))

    # create df
    df = pd.DataFrame(data)
    # clean data, replace '--' with NaN, convert to float
    df = df.replace('--', 'NaN').astype(dtypes)
    # add column '代号', e.g. '英镑(GBP)' -> 'GBP'
    df['代号'] = df['币种'].str.extract(r'\((\w+)\)')
    # modify column '币种', e.g. '英镑(GBP)' -> '英镑'
    df['币种'] = df['币种'].str.extract(r'(.+)\(')
    # parse column '发布时间', e.g. '2023年04月01日 04:14:05' -> '2023-04-01 04:14:05', and convert to datetime
    df['发布时间'] = pd.to_datetime(
        df['发布时间']
            .str.replace(r'年|月', '-', regex=True)
            .str.replace(r'日', '', regex=True)
    )
    # reorder columns, move '代号' to the first column
    df = df[list(df.columns[-1:]) + list(df.columns[:-1])]

    logger.info(f"Successfully parsed the html content: \n{df}")
    return df


def parse_csv(csv: Optional[str]) -> Optional[pd.DataFrame]:
    # parse csv
    df = pd.read_csv(csv, header=0, index_col=None)
    # parse column '发布时间', e.g. '2023年04月01日 04:14:05' -> '2023-04-01 04:14:05', and convert to datetime
    df['发布时间'] = pd.to_datetime(
        df['发布时间']
            .str.replace(r'年|月', '-', regex=True)
            .str.replace(r'日', '', regex=True)
    )
    logger.info(f"Successfully parsed the csv content: \n{df}")
    return df


if __name__ == '__main__':
    # with open('.temp/test.html', 'r', encoding='utf-8') as f:
    #     out = parse_html(f.read())
    #
    # print(out.dtypes)
    # print(out['代号'].unique())
    # print(out['发布时间'].iloc[0].strftime('%Y_%m_%d-%H_%M_%S'))

    out = parse_csv('../assets/2023_04_01-04_14_05.csv')
    print(out.dtypes)

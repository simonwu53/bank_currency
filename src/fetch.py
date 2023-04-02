import requests
from typing import Optional
try:
    from .utils import get_logger
except ImportError:
    from utils import get_logger


logger = get_logger('url_fetch', filename='fetch.log')


def fetch_html_content(url: str) -> Optional[str]:
    response = requests.get(url)
    if response.status_code == 200:
        logger.info(f"Successfully loaded the website: {url}")
        return response.text
    else:
        logger.error(f"Failed to load the website: {response.status_code}")
        return None


if __name__ == '__main__':
    html_content = fetch_html_content(
        url="https://www.icbc.com.cn/ICBCDynamicSite/Optimize/Quotation/QuotationListIframe.aspx"
    )
    if html_content is not None:
        with open('.temp/test.html', 'w', encoding='utf-8') as f:
            f.write(html_content)

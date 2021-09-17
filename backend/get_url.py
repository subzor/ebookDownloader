import requests
from bs4 import BeautifulSoup

def get_ebook_name(que, url, ebook_name):

    headers = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36 Edg/89.0.774.77",
    "action": "sign-in"
    }
    try:
        requests_session = requests.Session()
        requests_session.headers = headers
        page = requests_session.get(url, headers=headers)
        soup = BeautifulSoup(page.content, 'lxml',from_encoding=page.encoding)
    except Exception as error:
        print(error)
    
    name = soup.title.string

    if ebook_name in name:
        que.put(url)

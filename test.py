from datetime import time

from bs4 import BeautifulSoup

import requests

import pymysql


rsp = requests.get("https://www.qidian.com/all/").text
soup = BeautifulSoup(rsp, "html.parser")
print(soup.get_text())
print(soup)

from datetime import time

from bs4 import BeautifulSoup

import requests

import pymysql


# rsp = requests.get("https://www.qidian.com/all/").text
# soup = BeautifulSoup(rsp, "html.parser")
# print(soup.get_text())
# print(soup)

class GetBookMessage:

    def __init__(self):
        self.baseurl = 'https://www.qidian.com/all/'

    def getbstype(self, url):
        rsp = requests.get(url).text
        soup = BeautifulSoup(rsp, "html.parser")

        return soup  # soup对象

    def draw_base_list(self, url):
        soup = self.getbstype(url)
        listt = soup.find('div', class_="book-img-text").find_all('div', class_='book-mid-info')
        for x in listt:
            self.book_name = x.find('h2').text.strip()  # 书名
            self.author = x.find('p', class_='author').find(class_='name').text.strip()  #
            self.main_type = x.find('p', class_='author').find('a', class_='').text.strip()  # 小说的主类型
            self.second_type = x.find('p', class_='author').find('a', class_='go-sub-type').text.strip()  # 小说的副类型
            self.book_status = x.find('p', class_='author').find('span').text.strip()  # 小说更新的状态
            self.brief_intro = x.find('p', class_='intro').text.strip()
            self.latest_chapter = x.find('p', class_='update').find('a').text.strip()
            self.dict_data()  # 调用生成字典的函数


    def draw_second_list(self,url):
        soup = self.getbstype(url)
        listt2 = soup.find('div', class_="book-img-text").find_all('div', class_='book-img-box')
        for x in listt2:
            self.pic_url = 'https:' + x.find('a').find('img')['src']
            self.dict_data_second()


    def dict_data(self):

        data = {
            'book_name': self.book_name,
            'author': self.author,
            'main_type': self.main_type,
            'second_type': self.second_type,
            'book_status': self.book_status,
            'brief_intro': self.brief_intro,
            'latest_chapter': self.latest_chapter
        }
        print(data)
        self.write_to_MySQL(data, "finalpoint", "book_new")  # 写入数据库
        pass


    def dict_data_second(self):

        data = {
            'pic_url': self.pic_url
        }
        print(data)
        self.write_to_MySQL(data, "finalpoint", "book_new")  # 写入数据库
        pass

    def write_to_MySQL(self, dic, database, table_name):
        keys = ', '.join(dic.keys())
        values = ', '.join(['% s'] * len(dic))  # 动态的构造占位符
        db = pymysql.connect(host='localhost', user='root', password='507624', port=3306, db=database)  # 连接数据库
        cursor = db.cursor()  # 数据库连接对象
        sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table_name, keys=keys, values=values)  # 插入语句
        # cursor.execute(sql, tuple(dic.values()))
        try:
            if cursor.execute(sql, tuple(dic.values())):
                print('Successful')
                db.commit()  # commit是把查询语句提交到数据库内
        except:
            print('Failed')
            db.rollback()
        cursor.close()  # 关闭对象
        db.close()  # 关闭数据库释放资源


if __name__ == '__main__':
    """主函数"""
    url = "https://www.qidian.com/all/"
    drawBook = GetBookMessage()
    drawBook.draw_base_list(url)
    drawBook.draw_second_list(url)
    for x in range(1, 5):
        drawBook.draw_base_list(drawBook.baseurl + 'page' + str(x))
        drawBook.draw_second_list(drawBook.baseurl + 'page' + str(x))

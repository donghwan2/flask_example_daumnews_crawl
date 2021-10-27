from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import pandas as pd

# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import chromedriver_autoinstaller
import time

# # 엑셀 쓰기 위한 준비
# write_wb = Workbook()
# write_ws = write_wb.active
# write_ws.cell(1,1,"안녕")
# write_wb.save("result.xlsx")

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

# 다음 뉴스 크롤링
@app.route('/result', methods=['POST'])
def result():

    keyword = request.form['input1']
    page = request.form['input2']

    # https://search.daum.net/search?nil_suggest=btn&w=news&DA=PGD&q=%EC%95%88%EB%85%95&p=1

    daum_list = []

    for i in range(1, int(page)+1):
        print("page: ", i)
        # 뉴스 검색 url + 검색어
        req = requests.get("https://search.daum.net/search?nil_suggest=btn&w=news&DA=PGD&q={}&p={}".format(keyword, str(i)))
        soup = BeautifulSoup(req.text, 'html.parser')

        for i in soup.find_all("a", class_="tit_main fn_tit_u"):
            print(i.text)
            daum_list.append(i.text)
        print('\n')
    
    df = pd.DataFrame({'제목':daum_list})
    df.to_excel('static/result.xlsx')
    return render_template("result.html", daum_list=daum_list)

# 네이버 쇼핑 크롤링
# @app.route('/naver_shopping')
# def naver_shopping():
#     # 셀레니움 크롤링
#     chrome_path = chromedriver_autoinstaller.install()
#     driver = webdriver.Chrome(chrome_path)
#     driver.implicitly_wait(3)

#     driver.get("https://search.shopping.naver.com/search/all?query=%EB%A7%8C%EB%91%90&frm=NVSHATC&prevQuery=%EB%A7%8C%EB%91%90")
#     soup = BeautifulSoup(driver.page_source, 'html.parser')
#     print(soup)

#     return render_template("shopping.html")

if __name__ == '__main__':
    app.run()


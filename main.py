import requests
import schedule
import time
import pymysql
from bs4 import BeautifulSoup
# def job():
conn = pymysql.connect(host='127.0.0.1', user='kops***', password='********', db='gecko', charset='utf8')
curs = conn.cursor()
for j in range(4, 9):
    url = 'https://www.coingecko.com/en?page='+str(j)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        names = soup.find_all('a', {'class': 'tw-hidden lg:tw-flex font-bold tw-items-center tw-justify-between'});
        ranks = soup.find_all('td', {'class': 'table-number tw-text-left text-xs'});
        prices = soup.find_all('td', {'class': 'td-market_cap cap col-market cap-price text-right'});
        sql = '';
        for i in range(0, 100):
            sql = 'insert into gecko_rank(ID,  RANKING, NAME, price, DATE  ) values(NULL,  '+ranks[i].get_text().strip() \
                  + ',\''+ names[i].get_text().strip() \
                  +'\',' + prices[i].get_text().strip().replace('$','').replace(',','') \
                  +', now()); '
            print(sql)
            curs.execute(sql)

    else :
        print(response.status_code)
conn.commit()
curs.close()
conn.close()

# schedule.every().day.at("21:51").do(job)# 4시간마다 job 실행
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

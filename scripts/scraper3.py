# scraper final
import re
import urllib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
# import telegram
# from . import telegram_info # django_extentsions 설치 전
import secret # django_extentsions 설치 후
from hotdeal.models import Deal
from datetime import datetime, timedelta
import time

# TLGM_BOT_API = secret.TLGM_BOT_API

# tlgm_bot = telegram.Bot(token = TLGM_BOT_API)
# DB 테이블 데이터 유지기간 설정 변수
during_date = 3
# DB 테이블 저장을 위한 추천 갯수
up_cnt_limit = 0
# 환율 API
url_usd = "https://finance.naver.com/marketindex/"
res_usd = urllib.request.urlopen(url_usd).read()
soup_usd = BeautifulSoup(res_usd, "html.parser")
usd = soup_usd.find('select', id="select_to", class_="selectbox-source")
currency ={}
for opt in usd.find_all('option'):
    currency[opt.text[-3:]]=float(opt['value'])
us = currency['USD']
jp = currency['JPY']

category_dict = {
    "IT" : ["PC/하드웨어", "노트북/모바일", "게임/SW", "컴퓨터", "디지털", "SW/게임", "PC제품"],
    "상품권" : ["상품권/쿠폰", "상품권", "모바일/상품권"],
    "가전/가구" : ["가전/TV", "가전/가구", "가전제품"],
    "생활/식품" : ["생활/식품", "디지털", "식품/건강", "먹거리", "생활용품"],
    "의류/잡화/서적" : ["패션/의류", "서적", "의류/잡화",  "의류" ],
    "기타" : ["기타"],
    "화장품" : ["화장품"],
    "패키지/이용권" : ["패키지/이용권"],
    "해외핫딜" : ["해외핫딜"]
}

def quasarzone_crowling(url):
    for i in range(1, 5):
        time.sleep(0.31)
        url = "https://quasarzone.com/bbs/qb_saleinfo?page="
        url = url + str(i)
        print(url)
        res = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) # request를 날려서 받은 값을 res라는 변수에 저장
        res = urlopen(res)

        soup = BeautifulSoup(res, "html.parser") # html로 parsing 해라

        items = soup.select("div.market-type-list > table > tbody > tr")

        #DB 테이블에 3일치만 유지한다 => 3일 전 데이터는 delete 시킨다
        # row, _ = Deal.objects.filter(upload_date__lte=datetime.now() - timedelta(hours=during_date)).delete()

        for item in items:
            try:
                img_url = item.select("td > div.market-info-list > div.thumb-wrap > a.thumb > img.maxImg")[0].get("src").strip() # src : 속성 # strip() : 양쪽 공백 제거
                
                link = item.select("td > div.market-info-list > div.market-info-list-cont > p.tit > a.subject-link > span.ellipsis-with-reply-cnt")[0].parent.get("href").strip() # parent : 특정 요소의 부모 요소를 가져옴
                link = "https://quasarzone.com/" + link
                                    
                res_2 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
                res_2 = urlopen(res_2)
                
                soup_2 = BeautifulSoup(res_2, "html.parser")

                
                title = soup_2.select("div.common-view-wrap > div.common-view-area > dl > dt > div > h1.title")[0].text.strip()
                title = re.sub("진행중|인기|종료", "", title).lstrip()

                category = item.select("td")[1]
                category = category.select("div.market-info-list > div.market-info-list-cont > div.market-info-sub > p > span.category")[0].text.strip()

                category = [key for key,value in category_dict.items() if category in value]
                if category != []:
                    category = category[0]
                    
                price = item.select("div.market-info-list > div.market-info-list-cont > div.market-info-sub > p > span > span.text-orange")[0].text.strip()
                price = price.replace(",", "")
                
                if price[0] == "$" :
                    price = price[2:]
                    price = price[:-6]
                    price = price.replace(".", "")
                    price = int(int(price) * us)
                    
                elif price[0] == "¥" :
                    price = price[2:]
                    price = price[:-6]
                    price = int(int(price) * jp)
                    
                else:
                    price = price[2:]
                    price = price[:-6]
                    price = int(price)

                upload_date = soup_2.select("div.common-view-wrap > div.common-view-area > dl > dt > div.util-area > p.right > span.date")[0].text.strip()
                date_time = datetime(year = int(upload_date[:4]), month=int(upload_date[5:7]), day=int(upload_date[8:10]), hour=int(upload_date[11:13]), minute=int(upload_date[14:16]))

                
                db_link_cnt = Deal.objects.filter(title__iexact=title).count()

                if db_link_cnt==0:
                    # chat_id = secret.chat_id
                    # message = title
                    # tlgm_bot.sendMessage(chat_id, message)
                #     # 스크래핑 결과를 DB의 Deal 테이블에 저장
                    # print(type(img_url), type(category), type(title), type(price), type(link), type(reply_count), type(up_count), type(upload_date))
                    print(upload_date)
                    Deal(image=img_url, category=category, title=title, price=price, link=link, upload_date=date_time,site="quasarzone").save()
                
            except Exception as e: # 비어있으면 그냥 지나가라
                continue
            
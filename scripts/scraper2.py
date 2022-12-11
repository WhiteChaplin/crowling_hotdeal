
#에펨코리아 핫딜 게시판 크롤링.
#list_index, image, title, link, reply_count, up_count, upload_date, category, price
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime
from hotdeal.models import Deal
import time
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
def epem_crowling(input_url):
    base_url = "https://www.fmkorea.com/"
    # url = 'https://www.fmkorea.com/index.php?mid=hotdeal&sort_index=pop&order_type=desc'
    for index in range(1,4):
        url = input_url+"&page="+str(index)
        time.sleep(1)
        res = requests.get(url)
        print(f"epem: {res}")
        # print(int(res.headers["Retry-After"]))
        soup = BeautifulSoup(res.text,"html.parser")
        items = soup.select("div.fm_best_widget>ul>li.li_best2_hotdeal0")
        # print(items)
        #일단 중간에 삭제된 url이 있으면 hotdeal_var8Y가 되어버림. 없는 값 처리 해야함
        for item in items:
            #DB 테이블에 3일치만 유지
            row, _ = Deal.objects.filter(upload_date__lte=datetime.now() - timedelta(days=during_date)).delete()
            try:
                if item.select("a.hotdeal_var8") != []:
                    img = ""
                    if item.select("img.thumb") != []:
                        img = item.select("img.thumb")[0].get("data-original").strip()

                    link = base_url+item.select("h3.title>a")[0].get("href").strip()
                    # reply_count = item.select("h3.title>a>span.comment_count")[0].text.strip().replace("[","").replace("]","")
                    # print(item.select("span.count"))
                    up_count = 0
                    if item.select("span.count") != []:
                        up_count = int(item.select("span.count")[0].text.strip().replace("[","").replace("]",""))
                    # print(up_count)
                    in_res = requests.get(link)
                    soup = BeautifulSoup(in_res.text,"html.parser")

                    
                    if soup.select("div.top_area>span.date") != []:
                        inner_info = soup.select("div.top_area>span.date")[0].text
                    print(inner_info)
                    date_time = datetime(year = int(inner_info[:4]), month=int(inner_info[5:7]), day=int(inner_info[8:10]), hour=int(inner_info[11:13]), minute=int(inner_info[14:16]))
                    
                    title = ""
                    if item.select("a.hotdeal_var8") != []:
                        title = item.select("a.hotdeal_var8")[0].text.strip()
                    index_num = 0
                    for index in title[::-1]:
                        if index != "[":
                            index_num+=1
                        else:
                            break
                    title = title[:len(title)-index_num-1]
                    #shopping_mall = item.select("div.hotdeal_info>span>a.strong")[0].text.strip() #쇼핑몰
                    
                    price = ""
                    if item.select("div.hotdeal_info>span>a.strong"):
                        price = item.select("div.hotdeal_info>span>a.strong")[1].text.strip() #가격
                    price_raw = "" #가격
                    
                        
                    for index in price:
                        try:
                            if index == ",":
                                continue
                            elif index == "원":
                                break
                            elif type(int(index)):
                                price_raw+=index
                        except Exception as e:
                            continue
                    if price_raw == "":
                        price_raw = 0
                    else:
                        # print(price_raw)
                        price_raw = int(price_raw)
                    category = item.select("div>span.category>a")[0].text.strip().replace("[","").replace("]","") #카테고리
                    category = [key for key,value in category_dict.items() if category in value]
                    if category != []:
                        category = category[0]
                    # print("제목: ",title, "/ 쇼핑몰: ",shopping_mall ,"/ 가격: ",price_raw,"/ 카테고리: ", category)
                    # print(price_raw)
                    # print(date_time)
                    
                    if up_count >=0:
                        if(Deal.objects.filter(title__iexact=link).count()==0):
                            Deal(image = img, title = title, link = link, upload_date = date_time,category = category, price = price_raw, site = "epem_korea").save()
            
            except Exception as e: # 비어있으면 그냥 지나가라
                continue
# epem_crowling('https://www.fmkorea.com/index.php?mid=hotdeal&sort_index=pop&order_type=desc')
            
    #메인 페이지를 크롤링할 py 파일과 같은 폴더에 두고 메인 페이지에서 카테고리나 가격, 검색 일자 구간을
    #입력하고 그 입력한 값을 얻기위해 메인 페이지를 크롤링해 변수에 값을 저장하고 
    #메인 크롤링을 실행할 파일에서 크롤링 기능을 클래스나 함수로 정의하고 파라미터로 메인페이지에서
    #설정한 값들을 넘겨서 크롤링 실행할 계획.
    # page = open("test.html",'r').read()
    # soup = BeautifulSoup(page,"html.parser")
    # print(soup.select("h1")[0].text)
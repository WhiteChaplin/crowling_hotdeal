
#https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu
import requests
from bs4 import BeautifulSoup
# telegram 라이브러리 import
import telegram
from hotdeal.models import Deal
from datetime import datetime, timedelta
import time
import secret #django 젤 상위폴더이기 때문에 바로 사용 가능. django에서 매핑해줌
from scripts import scraper2
from scripts import scraper3
#설치 후
# import secret
TLGM_BOT_TOKEN = secret.TLGM_BOT_TOKEN
tlgm_bot = telegram.Bot(token=TLGM_BOT_TOKEN) #봇의 url 토큰 지정
print(tlgm_bot)

url_dict = {
    "ppoumpu":"https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu",
    "epem":'https://www.fmkorea.com/index.php?mid=hotdeal',
    "quasarzone":"https://quasarzone.com/bbs/qb_saleinfo?page="
}

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

#DB 테이블 데이터 유지기간 설정 변수
during_date = 3

#DB 테이블 지정을 위한 추천 갯수 지정
up_cnt_limit = 1

def run():
    for key,value in url_dict.items():
        if key == "ppoumpu":
            for index in range(1,3):
                print("time wake")
                url = value+"&page="+str(index)
                print(url)
                res = requests.get(url)
                print(res)
                # soup = BeautifulSoup(open("hotdeal/templates/index.html",'r'), "html.parser")
                soup = BeautifulSoup(res.text,"html.parser")

                items = soup.select("tr.list1, tr.list0")

                for item in items:
                    
                    #DB 테이블에 3일치만 유지
                    row, _ = Deal.objects.filter(upload_date__lte=datetime.now() - timedelta(days=during_date)).delete()
                    # row, _ = Deal.objects.filter(upload_date__lte=datetime.now() - timedelta(minutes=during_date)).delete()
                    # print(row)
                    try:
                        img_url = item.select("img.thumb_border")[0].get("src").strip()

                        title = item.select("a font.list_title")[0].text.strip() #a 태그 내 font태그에서 class이름이 list_title인 것. a 태그 지정 안하고 바로 font 태그로 지정해도 가능
                        link = item.select("a font.list_title")[0].parent.get("href").strip()
                        link = link.replace("/zboard/", "") #만약 미리 zboard가 입력되어 있으면 공백으로 처리
                        link = link.lstrip('/') 
                        link= "https://www.ppomppu.co.kr/zboard/" + link #최종 link를 만듬.

                        replay_count = item.select("td span.list_comment2 span")[0].text.strip()

                        up_count = item.select("td.eng.list_vspace")[2].text.strip()

                        up_count = up_count.split("-")[0]
                        up_count = int(up_count)

                        
                        in_res = requests.get(link)
                        soup = BeautifulSoup(in_res.text,"html.parser")
                        inner_info = soup.select("div.sub-top-text-box")
                        start_index = inner_info[0].text.find("등록일")
                        insert_date = inner_info[0].text[start_index+5:start_index+21]

                        date_time = datetime(year = int(insert_date[:4]), month=int(insert_date[5:7]), day=int(insert_date[8:10]), hour=int(insert_date[11:13]), minute=int(insert_date[14:16]))
                        list_index = int(item.select("td.eng.list_vspace")[0].text.strip()) #글번호
                        
                        category = item.select("td.list_vspace>table>tr>td")[1]
                        category = category.select("div>span")[1].text.strip().replace("[","").replace("]","")
                        
                        # print(category.replace("[","").replace("]",""))
                        
                        category = [key for key,value in category_dict.items() if category in value]
                        if category != []:
                            category = category[0]
                        
                        print(category, up_count)
                        # money_slice = title.find("원")
                        # money = 0
                        
                        # for text in reversed(title[:money_slice]):
                        #     if
                        # print(title[:money_slice+1])
                        if up_count >=up_cnt_limit:

                                if(Deal.objects.filter(link__iexact=link).count()==0):
                                    print(title)
                                    Deal(image = img_url, title = title, link = link, upload_date = date_time,category = category, price = 0,site="ppomppu").save()
                                    caht_id = secret.chat_id #발급받은 채팅방 id
                                    message = f"{title}--{link}" #크롤링해서 가져온 제목과 링크를 message로 지정
                                    tlgm_bot.sendMessage(caht_id, message)
                            
                    #공백. 값이 없는 것 처리. 값이 없으면 패스한다.
                    except Exception as e:
                        continue
                    
                time.sleep(0.31)
        elif key == "epem":
            scraper2.epem_crowling(value)
        elif key == "quasarzone":
            scraper3.quasarzone_crowling(value)
    
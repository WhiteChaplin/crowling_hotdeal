#https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu
import requests
from bs4 import BeautifulSoup
#telegram 라이브러리 import
import telegram

from .. import secret
TLGM_BOT_TOKEN = secret.TLGM_BOT_TOKEN
tlgm_bot = telegram.Bot(token=TLGM_BOT_TOKEN) #봇의 url 토큰 지정
url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
res = requests.get(url)



soup = BeautifulSoup(res.text, "html.parser")
print(soup) #똑같이 html 문서가 출력되나 프로그램 내부적으로 태그나 클래스 이름의 요소 지정이 가능해진다.
items = soup.select("tr.list1, tr.list0")
# print(items)
#가지고 와야 하는 것 : img_url, title, link, replay_count(반응 갯수), up_count(추천 갯수)
for item in items:
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
        # print(up_count)
        
        if up_count >=3:
            # 터미널 프린트
            print(img_url, title, link, replay_count, up_count)
            #텔레그렘의 bot에 전송
            caht_id = secret.chat_id #발급받은 채팅방 id
            message = f"{title}--{link}" #크롤링해서 가져온 제목과 링크를 message로 지정
            tlgm_bot.sendMessage(caht_id, message)
            
    #공백. 값이 없는 것 처리. 값이 없으면 패스한다.
    except Exception as e:
        continue
    
# print(soup.select_one("#revolution_main_table > tbody > tr:nth-child(12) > td:nth-child(3) > table > tbody > tr > td:nth-child(2) > div > a > font.list_title").text)
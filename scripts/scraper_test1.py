#https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu
import requests
from bs4 import BeautifulSoup

# url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
url = "https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu&page=2&divpage=75"
res = requests.get(url)
# print(res) #response 200이 출력. 정상적으로 접속했다는 의미
# print(res.text) #해당 url 페이지의 html 문서를 가져옴

#html 문서를 넣어주고 html 문서로 parsing하라는 의미이다.
soup = BeautifulSoup(res.text, "html.parser")
# print(soup) #똑같이 html 문서가 출력되나 프로그램 내부적으로 태그나 클래스 이름의 요소 지정이 가능해진다.
items = soup.select("tr.list1, tr.list0")
# print(items)
#가지고 와야 하는 것 : img_url, title, link, replay_count(반응 갯수), up_count(추천 갯수)
for item in items:
    try:
        img_url = item.select("img.thumb_border")[0].get("src").strip()
        #title은 src 속성 안에 있는 것이 아닌 그냥 일반적인 text이기 때문에 .text를 하면 된다.
        title = item.select("a font.list_title")[0].text.strip() #a 태그 내 font태그에서 class이름이 list_title인 것. a 태그 지정 안하고 바로 font 태그로 지정해도 가능
        #link는 좀 난해하다. parent 속성을 알아야 한다. 특정 요소가 클래스나 id가 없을 시 사용
        #href는 font.list_title을 감싸고 있기 때문에 이거를 감싸는(부모 요소인) parnet를 사용해서 요소에 접근한다.
        #실제 입력되는 주소는 https://www.ppomppu.co.kr/zboard/ 뒤에 link가 되어야 한다.
        #view.php?id=ppomppu&page=1&divpage=75&no=444053 일반적으로 link를 긁어왔을 때 보여지는 것.
        #https://www.ppomppu.co.kr/zboard/view.php?id=ppomppu&page=1&divpage=75&no=444034
        link = item.select("a font.list_title")[0].parent.get("href").strip()
        link = link.replace("/zboard/", "") #만약 미리 zboard가 입력되어 있으면 공백으로 처리
        link = link.lstrip('/') 
        link= "https://www.ppomppu.co.kr/zboard/" + link #최종 link를 만듬.
        #얘는 td 태그 내 span태그 중 classname이 list_comment2인 태그 내 span 태그의 text로 지정되어있음.        
        replay_count = item.select("td span.list_comment2 span")[0].text.strip()
        #up_count는 추천수로 td 태그 내 클래스 이름이 eng list_vspace인 것의 리스트를 가져옴.
        #조회수는 3, 1은 시간. 0은 글번호
        #저기 td 태그를 가보면 class가 eng list_vspace로 되어있다. 이것은 클래스 이름이 2개인 것으로 eng도 적용되고 list_vspace로 적용되는데
        #둘다 class_name을 적용해서 사용할 때 이렇게 사용한다.
        up_count = item.select("td.eng.list_vspace")[2].text.strip()
        #첫번째 있는 것이 추천수 [1]이 다른의견이다.
        up_count = up_count.split("-")[0]
        up_count = int(up_count)
        # print(up_count)
        
        # category = item.select("td.list_vspace>table>tr>td>div>span")
        category = item.select("td.list_vspace>table>tr>td")[1]
        category = category.select("div>span")[1].text.strip()
        print(category.replace("[","").replace("]",""))
        # print(category)
        
        # if up_count >=3:
            # 터미널 프린트
            # print(img_url, title, link, replay_count, up_count)
            
    #공백. 값이 없는 것 처리. 값이 없으면 패스한다.
    except Exception as e:
        continue
    
# print(soup.select_one("#revolution_main_table > tbody > tr:nth-child(12) > td:nth-child(3) > table > tbody > tr > td:nth-child(2) > div > a > font.list_title").text)
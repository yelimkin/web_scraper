# 웹 크롤링하는 사이트
# https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu

import requests
from bs4 import BeautifulSoup

url = 'https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu'
res = requests.get(url)

# print(res.text)

# res.text는 문자열이므로 BeautifulSoup 객체에 넣어 html 파일로 만들어 준다.
soup = BeautifulSoup(res.text, "html.parser")
# print(soup)

# tr 태크의 list1 클래스인 데이터 가져오기
items = soup.select("tr.list1, tr.list0")
# print(items) # 리스트 형태

# img_url, title, link, reply_count, up_count
for item in items:
    try:
        img_url = item.select("img.thumb_border")[0].get("src").strip()
        # 각 요소의 src 속성 값 가져오기
        # strip 공백 제거
        # print(img_url)

        title = item.select("a font.list_title")[0].text.strip()
        # 그 태그의 실제적인 문자열을 가져오려면  text
        # print(title)

        link = item.select("a font.list_title")[0].parent.get("href").strip()
        # 클래스 정의가 없을 경우 특정 클래스 태그의 부모 요소는 parent로 가져올 수 있다.
        link = link.replace("/zboard/", "").lstrip()
        link = 'https://www.ppomppu.co.kr/zboard/' + link
        # print(link)

        reply_count = item.select("span.list_comment2 span")[0].text.strip()
        # print(reply_count)

        up_count = item.select("td.eng.list_vspace")[-2].text.strip().split(" - ")[0]
        # 태그의 클래스가 여러 개일 경우 .으로 두 클래스를 연결해준다.
        up_count = int(up_count)
        # print(up_count)

        if up_count >= 3:
            print(img_url, title, link, reply_count, up_count)
            
    except Exception as e:
        continue
# 웹 스크래핑 코드
# 텔레그램 push
# django로 DB 저장하기
from hotdeal.models import Deal

# 웹 크롤링하는 사이트
# https://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu

import requests
from bs4 import BeautifulSoup
import telegram
# import telegram_info as ti # django_extensions 설치하기 전
# from . import telegram_info as ti # django_extensions 설치하기 후
import env_info as ti
from datetime import datetime, timedelta

# DB 데이블 데이터 유지 기간 설정 변수
during_date = 3
# 추천 수 기준 지정
up_cnt_limit = 3

TLGM_BOT_TOKEN = ti.TLGM_BOT_TOKEN
tlgm_bot = telegram.Bot(token=TLGM_BOT_TOKEN)

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
def run():
    # 최근 3일 데이터만 DB에 저장하고 유지
    # 삭제한 데이터 개수 -> row
    # row, _ = Deal.objects.filter(cdate__lte = datetime.now() - timedelta(days=3)).delete()
    row, _ = Deal.objects.filter(cdate__lte = datetime.now() - timedelta(minutes=during_date)).delete()
    print(row, "deals deleted")
    
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

            if up_count >= up_cnt_limit:
                # print(img_url, title, link, reply_count, up_count)

                # hotdeal 앱의 Deal 클래스를 통해 DB 테이블에 데이터 저장
                # link와 대소문자를 구분하지 않고 정확히 같은 데이터 찾기 -> '__iexact' 속성
                # DB에 저장된 link가 없다면
                db_link_cnt = Deal.objects.filter(link__iexact=link).count()
                if(db_link_cnt == 0): # 중복이 없는 것만 출력하고 저장하기
                    # 텔레그램 봇으로 push sendMessage(chat_id, 전송 메시지)
                    chat_id = ti.chat_id
                    message = link
                    tlgm_bot.sendMessage(chat_id, message)

                    Deal(img_url=img_url, title=title, link=link, reply_count=reply_count, up_count=up_count).save()

        except Exception as e:
            continue
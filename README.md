# Crawler

Nomad Coder Web Crawler including email crawling


(구글 이메일 기준)

아이디와 비밀번호를 입력하면 자동으로 Nomad Coder 챌린지 경과가 크롤링되는 프로그램입니다!

<img width="785" alt="image" src="https://user-images.githubusercontent.com/41983244/79634559-124fdf00-81a6-11ea-84da-385764a77ed1.png">



# 크롬드라이버 설치

실행하기 위해선 크롬브라우저와 크롬드라이버를 깔아주셔야 합니다 !!

(DIRECT URL : https://chromedriver.storage.googleapis.com/index.html?path=81.0.4044.69/)

설치 URL : https://sites.google.com/a/chromium.org/chromedriver/



# CHROME_DRIVER 설치 위치 지정 예시

(Line 17)

CHROME_DRIVER = "/Users/{사용자이름}/Downloads/chromedriver"

압축해제된 chromedriver 가 존재하는 위치를 지정해주세요!



# import

requests

BeautifulSoup

selenium


저는 다음과 같은 방법으로 설치했습니다!
 : python3 -m pip install {모듈이름} --user


# 업데이트 (2020.04.22)

비밀번호 틀렸을 시 비밀번호 재입력 기능.

대기시간 없이 메일확인.

이메일 올때까지 메일함 재확인.

로그인 성공할 때까지 재실행.

각종 예외 처리 수정.

! 오류가 발생할 시에 메일이나 슬랙 메시지 부탁드려요 ! [ peinguin77@gmail.com / Seongjun Jang ]


# 범용성
챌린지 종류에 구분없이 크롤링가능하도록 구현했습니다!


파이썬 챌린지 -

(Line 22)CHALLENGE = 5

(Line 27)MAX = 598

JS 챌린지 -

(Line 22)CHALLENGE = 4

(Line 27)MAX = 784


CHALLENGE NUMBERING -

1 : Kokoa Clone Challenge

2 : ReactJS Challenge

3 : WeTube Clone Challenge

4 : VanillaJS Challenge

5 : Python Challenge



# 사용 IDE


VSCode

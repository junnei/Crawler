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


# 시간 조정 가능

작업이 너무 오래 걸려서 지루하시거나, 이메일이 너무 늦게 와서 작업이 어렵다고요 ?

걱정마세요 ! 대기시간도 바꿀 수 있습니다

(Line 54)

Sleep(30)

#초 단위로 원하는만큼 조정해주세요!



# 범용성
챌린지 종류에 구분없이 크롤링가능하도록 구현했습니다!

(Line 22)

#파이썬 챌린지

CHALLENGE = 5

1 : Kokoa Clone Challenge

2 : ReactJS Challenge

3 : WeTube Clone Challenge

4 : VanillaJS Challenge

5 : Python Challenge



# 사용 IDE


VSCode

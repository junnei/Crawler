import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.system("clear")

GMAIL = "https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin"

EMAIL_ADDRESS = ""
PASSWORD = ""

CHROME_DRIVER = "/Users/jun/Downloads/chromedriver"
GET_EMAIL_URL = "https://challenges.nomadcoders.co/users/login"
LOGIN_URL = ""

# 파이썬 챌린지 : 5
# JS 챌린지 : 4
CHALLENGE = 4

# 처음 참가자 수
# 파이썬 챌린지 : 598
# JS 챌린지 : 784
MAX = 784

# 현재 참가자 수
participants=0

# 크롤링데이터
data = []

# 과제 제출 실패 데이터
fail = []

# 로그인 성공 여부
session_Login = False

# 크롬드라이버 선언
driver = webdriver.chrome.webdriver.WebDriver

# 로그인을 위한 데이터 입력
def SetLogin():
    print("\t< Gmail Login >")
    global EMAIL_ADDRESS
    global PASSWORD
    EMAIL_ADDRESS = input("email : ")
    PASSWORD = input("password : ")

# 크롬드라이버 실행
def excuteDriver():
    global driver
    driver = webdriver.Chrome(CHROME_DRIVER)

# 크롤링 데이터 받아오기
def getData():
    # 정상적으로 실행될때 까지 반복
    while len(data)==0:
        try:
            html = linkToPage(CHALLENGE)
            addToList(html)
        except:
            continue

# 노마드코더 로그인 이메일 보내기
def sendEmail():
    global driver
    driver.implicitly_wait(3) # 로딩 최대 3초 기다리기

    # 이메일 받기 위한 작업
    driver.get(GET_EMAIL_URL) # 노마드코더 로그인
    driver.find_element_by_name('email').send_keys(EMAIL_ADDRESS) # 주소 입력
    driver.find_element_by_xpath('/html/body/main/main/div/form/button').click() # 이메일 보내기

# 노마드코더 로그인 이메일 받기
def getEmail():
    global LOGIN_URL
    global driver
    driver.implicitly_wait(3) # 로딩 최대 3초 기다리기
    #LOGIN_URL이 존재할때 까지 반복
    while True:
        # 로그인 성공한 세션이 있을 경우 바로 메일함으로 이동
        global session_Login
        if(session_Login == False):
            global PASSWORD
            driver.get(GMAIL) # Gmail 이동
            driver.find_element_by_name('identifier').send_keys(EMAIL_ADDRESS) # 주소 입력
            driver.find_element_by_id('identifierNext').click() # 다음버튼
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, "password"))) # 비밀번호 입력 대기

            driver.find_element_by_name('password').send_keys(PASSWORD) # 비밀번호 입력
            driver.find_element_by_id('passwordNext').click() # 다음버튼
            
            # 받은편지함 나올때 까지 대기. 실패할경우 로그인 재시도.
            try:
                WebDriverWait(driver, 5).until(EC.title_contains(('받은편지함'))) # 받은 편지함 로딩 대기
            except:
                print("Login failed. Retrying...") # 로그인 실패
                PASSWORD = input("password : ") # 비밀번호 재입력
                continue
            session_Login = True # 로그인 성공 세션 저장
        else:
            driver.get(GMAIL) # 메일함 이동
            WebDriverWait(driver, 5).until(EC.title_contains(('받은편지함'))) # 받은 편지함 로딩 대기

        # 메일함 목록에 메일이 없을 때 예외처리
        try:
            print("모든 이메일 확인중")
            emails = driver.find_elements_by_class_name("xT") # 모든 이메일 확인
            for email in emails: # 노마드코더에서 온 가장 최근의 로그인 이메일 리스트 열기
                if(email.find_element_by_class_name("y6").text=="Log in Nomad Challenges"):
                    email.click()
                    break
        except: # 이메일 존재 유무 예외처리
            print("이메일 아예 없어용")
            continue
        
        # 로그인 이메일 리스트 로딩 대기
        try:
            print("이메일 로딩 기다려욤")
            WebDriverWait(driver, 3).until(EC.title_contains(('Log in Nomad Challenges')))
        except:
            print("에러 : 메일 없음 or [로딩 3초 초과]")
            continue
        
        # 이메일 크롤링
        print("이메일 크롤링해욤")
        text_source = driver.page_source
        email_soup = BeautifulSoup(text_source,"html.parser")
        emails = email_soup.find("div",{"role":"list"}).find_all("div",{"role":"listitem"})
        for email in emails:
            body = email.text
            url = body.rfind('this:')+6
            LOGIN_URL = body[url:url+79]
        if(LOGIN_URL!=""):
            break
    print(LOGIN_URL)
    return LOGIN_URL

def linkToPage(Challenge):

    # 이메일에서 로그인 URL을 받아와서 이동
    global driver
    driver.get(getEmail())

    #Progress Report 접속
    driver.get(f"https://challenges.nomadcoders.co/challenges/{Challenge}/report")
    html = driver.page_source
    return html
    
def addToList(html):
    url_soup = BeautifulSoup(html,"html.parser")
    progress = url_soup.find_all("div",{"class":"report__row"})
    global participants
    for person in progress[1:]:
        participants+=1
        fail = person.find_all("span",{"class":"report__fail"})
        if(len(fail)>=2):
            continue
        reports = person.find_all("div",{"class":"report__cell"})
        items = []
        for report in reports:
            link = report.find("a", href=True)
            if link is None:
                item = report.find("span")
                items.append(item.get_text())
                continue
            items.append(link['href'])
        data.append(items)


def printList():
    global fail
    fail = [0] * (len(data[0])-1)
    for i in range(len(data)):
        print(f"# {i} \t{data[i][0]} :",end="")
        for j in range(1,len(data[i])):
            print(" ",end="")
            if(data[i][j].find("repl")!=-1):
                print("O",end="")
            else:
                if(data[i][j]=="X"):
                    fail[j-1] = fail[j-1] + 1
                print(f"{data[i][j]}",end="")
        print("\n")
    print(f"Total : {MAX}")
    print(f"Survivors : {len(data)}")
    print(f"Total 🔪💨 : {MAX-len(data)}")
    print(f"Total Survivors Rate : {round(len(data)/MAX*100)}%\n")

    print(f"People in List : {participants}")
    print(f"List's 🔪💨 : {participants-len(data)}")
    print(f"List's Survivors Rate : {round(len(data)/participants*100)}%\n")

    print(f"Failure in Assignment (from only Survivors) [First Absent]- ")
    for i in range(len(fail)):
        print(f"\tAssignment {i+1} : {fail[i]} \tFailure Rate (Failure/Survivors) : {round(fail[i]/len(data)*100)}%")

def checkList():
    id=input("\nInput ID : ")
    for i in range(len(data)):
        if(data[i][0]==id):
            print(f"\n{data[i][0]}님 Progress -")
            for j in range(1,len(data[i])):
                print(f"\tAssignment {j} : {data[i][j]}")
    print()

SetLogin()
excuteDriver()
sendEmail()
getData()
printList()
checkList()

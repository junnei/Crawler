import os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

os.system("clear")

GMAIL = "https://www.google.com/gmail/"

EMAIL_ADDRESS = ""
PASSWORD = ""

CHROME_DRIVER = "/Users/jun/Downloads/chromedriver"
GET_EMAIL_URL = "https://challenges.nomadcoders.co/users/login"
LOGIN_URL = ""

# 파이썬 챌린지
CHALLENGE = 5

# 처음 참가자 수
MAX = 598

# 현재 참가자 수
participants=0

# 크롤링데이터
data = []

# 과제 제출 실패 데이터
fail = []

def SetLogin():
    print("\t< Gmail Login >")
    global EMAIL_ADDRESS
    global PASSWORD
    EMAIL_ADDRESS = input("email : ")
    PASSWORD = input("password : ")

def linkToPage(Challenge):
    driver = webdriver.Chrome(CHROME_DRIVER)
    driver.implicitly_wait(3) # 로딩 최대 3초 기다리기

    # 이메일 받기 위한 작업
    driver.get(GET_EMAIL_URL) # 노마드코더 로그인
    driver.find_element_by_name('email').send_keys(EMAIL_ADDRESS) # 주소 입력
    driver.find_element_by_xpath('/html/body/main/main/div/form/button').click() # 이메일 보내기
 
    driver.implicitly_wait(10) # 로딩 최대 10초 기다리기

    sleep(30) # 이메일을 받기 위한 대기 시간 (초)

    # 이메일 확인
    driver.get(GMAIL) # Gmail 이동
    driver.find_element_by_name('identifier').send_keys(EMAIL_ADDRESS) # 주소 입력
    driver.find_element_by_id('identifierNext').click() # 다음버튼
    driver.implicitly_wait(3) # 로딩 최대 3초 기다리기

    driver.find_element_by_name('password').send_keys(PASSWORD) # 비밀번호 입력
    driver.find_element_by_id('passwordNext').click() # 다음버튼
    driver.implicitly_wait(3) # 로딩 최대 3초 기다리기

    # 받은편지함 나올때 까지 최대 10초 대기.
    WebDriverWait(driver, 10).until(EC.title_contains(('받은편지함')))

    # 이메일 크롤링
    text_source = driver.page_source
    email_soup = BeautifulSoup(text_source,"html.parser")
    emails = email_soup.find_all("div",{"class":"xT"})
    for email in emails:
        title = email.find("div",{"class":"y6"}).get_text()
        if (title == "Log in Nomad Challenges"):
            body = email.find("span",{"class":"y2"}).get_text()
            LOGIN_URL = body[body.find(':')+2:body.find('on your browser.')]
    
    
    # 로그인 URL로 이동하기
    driver.get(LOGIN_URL)

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
    print(f"Survivors : {len(data)}")
    print(f"Participants : {participants}")
    print(f"Today's 🔪💨 : {participants-len(data)}")
    print(f"Today's Survivors Rate : {round(len(data)/participants*100)}%\n")
    print(f"Total 🔪💨 : {MAX-len(data)}")
    print(f"Total Survivors Rate : {round(len(data)/MAX*100)}%\n")

    print(f"Failure in Assignment (from only Survivors) - ")
    for i in range(len(fail)):
        print(f"\tAssignment {i+1} : {fail[i]} \tFailure Rate (Failure/Survivors) : {round(fail[i]/len(data)*100)}%")

def checkList():
    id=input("\nInput ID : ")
    for i in range(len(data)):
        if(data[i][0]==id):
            print(f"{data[i][0]}님 Progress -")
            for j in range(1,len(data[i])):
                print(f"\tAssignment {j} : {data[i][j]}")

SetLogin()
html = linkToPage(CHALLENGE)
addToList(html)
printList()
checkList()

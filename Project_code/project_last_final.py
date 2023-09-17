# 2팀 코스모스 프로젝트

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wordcloud import WordCloud
from matplotlib import font_manager,rc
import time
import sys
import urllib
import math
import os
import pandas as pd
import xlwt
import re


def scroll_down(driver):
    driver.execute_script('window.scrollTo(0,document.body.scrollHeight);')
    time.sleep(1)

q=0 # 메뉴에서 종료(0 입력시)를 위한 응급처치
# 입력-----------------------------------------------------------------------------------------
while True:
    while True:
        print('메뉴')
        try:
            menu=int(input('1.검색키워드 입력 2.검색건수 입력 0.종료 : '))
            if menu>2 or menu<0:
                raise
        except:
            print('번호를 입력하세요.')
            print()
        else:
            if menu==1:
                while True:
                    print('ex : 응원, 감성, 재미있는, 감동적인')
                    keyword = input("검색할 키워드는 무엇입니까? : ")
                    if keyword=='':
                        print('키워드를 입력하세요.')
                        print()
                        continue
                    break
                while True:
                    try:
                        cnt=int(input('검색할 건수를 입력하세요.(1~2000) : '))
                        if cnt>10000 or cnt<0:
                            raise
                    except:
                        print('1~2000 사이의 숫자를 입력하세요.')
                        print()
                        continue
                    break
            if menu==2:
                while True:
                    try:
                        cnt=int(input('검색할 건수를 입력하세요.(1~2000) : '))
                        if cnt>10000 or cnt<0:
                            raise
                    except:
                        print('1~2000 사이의 숫자를 입력하세요.')
                        print()
                    break
                while True:
                    keyword = input("검색할 키워드는 무엇입니까? : ")
                    if keyword=='':
                        print('키워드를 입력하세요.')
                        print()
                        continue
                    break
            if menu==0:
                q=1
                break
        
            print()
            print('검색키워드 :',keyword)
            print('검색건수 :',cnt)
            print()
            while True:
                start=input('프로그램을 실행하겠습니까? (y/n) : ')
                if start=='y' or start=='Y' or start=='n' or start=='N':
                    break
                else:
                    print('y 혹은 n 을 입력해주세요.')
                    print()
                    continue
            if start=='n' or start=='N':
                print()
                print('메뉴로 돌아갑니다.')
                print()
                continue
            if start=='y' or start=='Y':
                break
    print('프로그램을 실행합니다.')
    print()



#인스타그램 데이터 수집----------------------------------------------------------------------------------------
    # 데이터수집 시작(시간)
    start_time=time.time()
    if q!=1:
        print('인스타그램에서',str(cnt)+'건의 데이터를 수집합니다.')
        print()

        # 로그인 실패 예외처리
        while True:
            # 인스타그램 로그인 페이지 접속
            path = 'Web_driver\\chromedriver.exe'
            driver = webdriver.Chrome(path)
            driver.get('https://www.instagram.com/')
            time.sleep(2)

            # 로그인 아이디,비밀번호 입력
            instar_id = input('인스타그램 아이디를 입력해 주세요 : ')
            instar_password = input('인스타그램 비밀번호를 입력해 주세요 : ')

            # id 입력
            id_input = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[1]/div/label/input')
            id_input.send_keys(instar_id)
            time.sleep(2)

            # password 입력
            password_input = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[2]/div/label/input')
            password_input.send_keys(instar_password)
            time.sleep(2)

            # 로그인 버튼 클릭
            login_btn = driver.find_element(By.XPATH,'//*[@id="loginForm"]/div/div[3]')
            login_btn.click()
            time.sleep(1)

            try:
                # 로그인 정보 저장 여부 표출 시 나중에 하기 클릭
                login_info_next = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'cmbtv')))# class name에 공백 존재 시 공백을 '.'로 대체
                login_info_next.click()

                # 알림 설정 화면 표출 시 나중에 하기 클릭
                setting_next = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'_a9--._a9_1')))# class name에 공백 존재 시 공백을 '.'로 대체
                setting_next.click()
                time.sleep(1)
            except:
                pass
        
            try:
                # 검색
                search = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME,'_aauy')))
                search.send_keys(keyword+'선물')
                time.sleep(6)
            except:
                print('아이디 / 비밀번호가 틀렸습니다.')
                driver.quit()
                continue
            else:
                break

        search.send_keys(Keys.ENTER)
        time.sleep(6)
        search.send_keys(Keys.ENTER) # ENTER를 2번 눌러야 검색이 됨
        time.sleep(10)

        # 검색된 게시물의 총 개수
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        post_cnt = soup.find('span','_ac2a').text.replace(',','')

        # 페이지 들어가기
        enter_page = driver.find_element(By.CLASS_NAME,'_aagw')
        enter_page.click()
        time.sleep(3)
        
        insta_list = []
        insta_tag_list = []
        insta_no=[]
        num = 1

        while True:
            # 해시 태그 검색
            # 현재 페이지 html 분석
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            try:
                hash_tag = soup.find('span','_aacl _aaco _aacu _aacx _aad7 _aade').find_all('a')
            except:
                pass
            else:
                time.sleep(1.5)
                
                for j in hash_tag:
                    insta_tag_list.append(j.get_text())
                
                insta_list.append(insta_tag_list)
                insta_tag_list = []

                insta_no.append(num)
                print(num,'건 진행완료')

                if num == 1:  # 다음 페이지로 이동(첫페이지한정)
                    next_page = driver.find_elements(By.TAG_NAME,'button')
                    next_page[3].send_keys(Keys.ENTER)

                if num == cnt: # 검색 건수 만큼만 크롤링
                    break

                elif num == int(post_cnt): # 검색된 양이 원하는 크롤링 양보다 적을 경우 최대한 하고 다음단계로 진행
                    print('검색된 게시물이 입력된 검색건수 보다 적습니다.')
                    break

                else:
                    next_page = driver.find_elements(By.TAG_NAME,'button') # 다음 페이지로 이동
                    next_page[4].click()
                time.sleep(2)
                num += 1

        print('인스타그램 데이터수집을 완료했습니다.')
        print()
        driver.quit()



    #카카오톡 선물하기 데이터수집---------------------------------------------------------------------------------- 
        print('카카오톡 선물하기에서',str(cnt)+'건의 데이터를 수집합니다.')
        print()

        # 검색 페이지 이동
        path = 'Web_driver\\chromedriver.exe'
        driver = webdriver.Chrome(path)
        driver.get("https://gift.kakao.com/search")
        time.sleep(1)

        # 검색하기
        search_txt = driver.find_element(By.ID,'searchInput')
        search_txt.click()

        # 검색키워드 보내기
        search_txt.send_keys(keyword+'선물')
        driver.find_element(By.CLASS_NAME,'sch_button').click()
        time.sleep(3)

        # 스크롤 높이
        last_height = driver.execute_script("return document.body.scrollHeight")
        num = 20
        while cnt > num : 
            # 끝까지 스크롤 다운
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            time.sleep(3)
            # 스크롤 다운 후 높이 다시 가져옴 
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
            num +=20

        try:
            full_html = driver.page_source
            soup = BeautifulSoup(full_html,'html.parser')
            content_list = soup.find('ul','list_prd').find_all('li')
        except:
            print('검색결과가 없어 메뉴로 돌아갑니다.')
            print()
            continue

        full_html = driver.page_source
        soup = BeautifulSoup(full_html,'html.parser')
        content_list = soup.find('ul','list_prd').find_all('li')

        kakao_list=[]
        kakao_no=[]
        no=1
        # 브랜드명 및 상품명 수집하기
        for item in content_list :

            if no == cnt+1:
                break
            else:
                product_brand = item.find('span','txt_brand').get_text()  #브랜드명
                product_name = item.find('strong','txt_prdname').get_text()  #상품명
                kakao_list.append([product_brand,product_name])
                kakao_no.append(no)
                no+=1
        
        print('카카오톡 선물하기 데이터수집을 완료했습니다.')
        time.sleep(2)
        driver.quit()
        
        # 수집 데이터 보여주기
        print(insta_list)
        print()
        print(kakao_list)
        print()

        # 데이터 수집 종료(시간)
        end_time=time.time()
        result_time=end_time-start_time
        print('모든 데이터 수집이 완료되었습니다.')
        print('데이터 수집부터 종료까지 걸린 소요시간은 총',str(round(result_time))+'초 입니다.')
        print()



    # 데이터 정제--------------------------------------------------------------------------------------------
        while True:
            print('제외시키고 싶은 검색어가 있습니까?')
            try:
                refine=int(input('1.재검색 2.제외검색어입력 3.다음단계 0.종료 : '))
                if refine<0 or refine>3:
                    raise
            except:
                print('번호를 입력하세요.')
                print()
            else:
                if refine==2:
                    refine2=input('제외할 검색어를 입력하세요 : ')
                    print(refine2)
                    print()
                    try:
                        for i in range(len(kakao_list)):
                            for j in range(len(kakao_list[i])):
                                refine3=kakao_list[i][j].find(refine2)
                                if refine3!=-1:
                                    kakao_list[i].clear()
                    except:
                        pass
                    try:
                        for i in range(len(insta_list)):
                            for j in range(len(insta_list[i])):
                                refine4=insta_list[i][j].find(refine2)
                                if refine4!=-1:
                                    insta_list[i].clear()
                    except:
                        pass
                if refine==3:
                    break
                if refine==1:
                    continue
                if refine==0:
                    break

        # 불필요한 글자 제거
        print('불필요한 특수문자를 제외합니다.')
        for i in range(len(kakao_list)):
            for j in range(len(kakao_list[i])):
                input_string = kakao_list[i][j]
                output_string = re.sub(r'[^\w\s]', '', input_string)
                kakao_list[i][j]=output_string
        for i in range(len(insta_list)):
            for j in range(len(insta_list[i])):
                input_string = insta_list[i][j]
                output_string = re.sub(r'[^\w\s]', '', input_string)
                insta_list[i][j]=output_string
        


    # 데이터 저장-------------------------------------------------------------------------------------------------
        real_name=[]
        while True:
            while True:
                print()
                save=input('추출한 데이터를 저장하시겠습니까? (y / n) : ')
                print()
                if save=='y' or save=='Y' or save=='n' or save=='N':
                    break
                else:
                    print('y 혹은 n 을 입력해주세요.')
                    print()
                    continue
            if save=='n' or save=='N':
                break

            while True:
                try:
                    save_menu=int(input('1.폴더선택 2.파일종류선택 3.파일이름선택 0.저장안함 : '))
                    print()
                    if save_menu>3 or save_menu<0:
                        raise
                except:
                    print('번호를 입력하세요')
                else:
                    if save_menu==1:
                        # 폴더 지정
                        print('(Default : crawling\\)')
                        f_dir=input('데이터를 저장할 폴더를 입력하세요. : ')
                        if f_dir=='':
                            f_dir='crawling\\'
                            f_dirtory=os.getcwd()+'\\'+f_dir
                        if not(os.path.isdir(f_dir)) :
                            os.makedirs(f_dir)
                            os.chdir(f_dirtory)
                            print("입력하신 경로가 존재하지 않아 %s 폴더에 생성했습니다." %f_dir)
                            print()
                        else :
                            os.chdir(f_dirtory)
                            print("%s 폴더에 생성했습니다." %f_dirtory)
                            print()
                        # 파일 종류 지정
                        while True:
                            print('저장할 파일의 종류를 입력하세요.')
                            try:
                                f_ext=int(input('1.csv 2.xlsx 3.txt : '))
                                if f_ext>3 or f_ext<1:
                                    raise
                            except:
                                print('번호를 입력하세요.')
                                print()
                            else:
                                break
                        # 파일 이름 지정
                        print()
                        f_name_kakao=input('(Default : kakao)카카오선물 데이터의 파일이름을 입력하세요. : ')
                        print()
                        f_name_insta=input('(Default : insta)인스타그램 데이터의 파일이름을 입력하세요. : ')
                        print()

                    if save_menu==2:
                        # 파일 종류 지정
                        while True:
                            print('저장할 파일의 종류를 입력하세요.')
                            try:
                                f_ext=int(input('1.csv 2.xlsx 3.txt : '))
                                if f_ext>3 or f_ext<1:
                                    raise
                            except:
                                print('번호를 입력하세요.')
                                print()
                            else:
                                break
                        # 폴더 지정
                        print('(Default : crawling\\)')
                        f_dir=input('데이터를 저장할 폴더를 입력하세요. : ')
                        if f_dir=='':
                            f_dir='crawling\\'
                            f_dirtory=os.getcwd()+'\\'+f_dir
                        if not(os.path.isdir(f_dir)) :
                            os.makedirs(f_dir)
                            os.chdir(f_dirtory)
                            print("입력하신 경로가 존재하지 않아 %s 폴더에 생성했습니다." %f_dir)
                            print()
                        else :
                            os.chdir(f_dirtory)
                            print("%s 폴더에 생성했습니다." %f_dirtory)
                            print()
                        # 파일 이름 지정
                        print()
                        f_name_kakao=input('(Default : kakao)카카오선물 데이터의 파일이름을 입력하세요. : ')
                        print()
                        f_name_insta=input('(Default : insta)인스타그램 데이터의 파일이름을 입력하세요. : ')
                        print()
                    if save_menu==3:
                        # 파일 이름 지정
                        print()
                        f_name_kakao=input('(Default : kakao)카카오선물 데이터의 파일이름을 입력하세요. : ')
                        print()
                        f_name_insta=input('(Default : insta)인스타그램 데이터의 파일이름을 입력하세요. : ')
                        print()
                        # 폴더 지정
                        print('(Default : crawling\\)')
                        f_dir=input('데이터를 저장할 폴더를 입력하세요. : ')
                        if f_dir=='':
                            f_dir='crawling\\'
                            f_dirtory=os.getcwd()+'\\'+f_dir
                        if not(os.path.isdir(f_dir)) :
                            os.makedirs(f_dir)
                            os.chdir(f_dirtory)
                            print("입력하신 경로가 존재하지 않아 %s 폴더에 생성했습니다." %f_dir)
                            print()
                        else :
                            os.chdir(f_dirtory)
                            print("%s 폴더에 생성했습니다." %f_dirtory)
                            print()
                        # 파일 종류 지정
                        while True:
                            print('저장할 파일의 종류를 입력하세요.')
                            try:
                                f_ext=int(input('1.csv 2.xlsx 3.txt : '))
                                if f_ext>3 or f_ext<1:
                                    raise
                            except:
                                print('번호를 입력하세요.')
                                print()
                            else:
                                break

                # 파일종류 정제
                if f_ext==1:
                    f_ext='.csv'
                if f_ext==2:
                    f_ext='.xlsx'
                if f_ext==3:
                    f_ext='.txt'

                # 파일이름 정제
                if f_name_kakao=='':
                    f_name_kakao='kakao'
                if f_name_insta=='':
                    f_name_insta='insta'

                file_name_kakao=f_dirtory+f_name_kakao+f_ext
                file_name_insta=f_dirtory+f_name_insta+f_ext

                i=1
                while os.path.exists(file_name_kakao):
                    file_name_kakao='%s%s(%d)%s' %(f_dir,f_name_kakao,i,f_ext)
                    i+=1
                j=1
                while os.path.exists(file_name_insta):
                    file_name_insta='%s%s(%d)%s' %(f_dir,f_name_insta,j,f_ext)
                    j+=1

                # 최종확인
                while True:
                    print(file_name_kakao)
                    print(file_name_insta)
                    check=input('이대로 저장하겠습니까? (y / n) : ')
                    if check=='y' or save=='Y' or save=='n' or save=='N':
                        break
                    else:
                        print('y 혹은 n 을 입력해주세요.')
                        print()
                        continue
                if check=='n' or check=='N':
                    print('파일 저장을 다시 시작합니다.')
                    print()
                    continue
                break
            if save_menu==0:
                break


            # 파일 저장
            kakao=pd.DataFrame()
            kakao['번호']=kakao_no
            kakao['브랜드명']=kakao_list
            kakao['상품명']=kakao_list

            insta=pd.DataFrame()
            insta['번호']=insta_no
            insta['해시태그']=insta_list

            if f_ext=='.csv':
                kakao.to_csv(file_name_kakao,encoding='utf-8-sig',index=False)
                insta.to_csv(file_name_insta,encoding='utf-8-sig',index=False)
            if f_ext=='.xlsx':
                kakao.to_excel(file_name_kakao)
                insta.to_excel(file_name_insta)
            if f_ext=='.txt':
                origin_stdout=sys.stdout
                f=open(file_name_insta,'a',encoding='UTF-8')
                sys.stdout=f
                time.sleep(1)
            
                for i in range(len(insta_no)):
                    print('번호',insta_no[i])
                    print(insta_list[i])
                    print()

                sys.stdout=origin_stdout
                time.sleep(1)
                f.close()

                origin_stdout=sys.stdout
                f=open(file_name_kakao,'a',encoding='UTF-8')
                sys.stdout=f
                time.sleep(1)
            
                for i in range(len(kakao_no)):
                    print('번호',kakao_no[i])
                    print(kakao_list[i][0])
                    print(kakao_list[i][1])
                    print()

                sys.stdout=origin_stdout
                time.sleep(1)
                f.close()
            break



    # 워드 클라우드---------------------------------------------------------------------------------------------------
        # 텍스트추출
        input_string = str(kakao_list)
        kakao = re.sub(r'[^\w\s]', '', input_string)
        input_string = str(insta_list)
        insta = re.sub(r'[^\w\s]', '', input_string)

        kakao=kakao.replace(str(keyword)+'선물','').replace(keyword,'').replace('선물','')
        insta=insta.replace(str(keyword)+'선물','').replace(keyword,'').replace('선물','')

        while True:
            while True:
                print()
                img_check=input('시각화를 진행합니까? (y / n) : ')
                if img_check=='y' or img_check=='Y' or img_check=='n' or img_check=='N':
                    break
                else:
                    print('y 혹은 n 을 입력해주세요.')
                    print()
                    continue
            if img_check=='n' or img_check=='N':
                break
                
            # 이미지파일 이름입력
            print()
            kakao_img_name=input('(Default : kakao)카카오선물 시각화 파일이름을 입력하세요. : ')
            print()
            insta_img_name=input('(Default : insta)인스타그램 시각화 파일이름을 입력하세요. : ')
            print()
            if kakao_img_name=='':
                kakao_img_name='kakao'
            if insta_img_name=='':
                insta_img_name='insta'

            # 이미지파일 디렉토리
            print('(Default : crawling\\)')
            img_dir=input('시각화 파일을 저장할 폴더를 입력하세요. : ')
            print()
            if img_dir=='':
                img_dir=f_dirtory
                
            img_ext='.jpg'

            kakao_img=img_dir+kakao_img_name+img_ext
            insta_img=img_dir+insta_img_name+img_ext

            i=1
            while os.path.exists(kakao_img):
                kakao_img='%s%s(%d)%s' %(img_dir,kakao_img_name,i,img_ext)
                i+=1
            j=1
            while os.path.exists(insta_img):
                insta_img='%s%s(%d)%s' %(img_dir,insta_img_name,j,img_ext)
                j+=1

            # 이미지파일 최종확인
            print(kakao_img)
            print(insta_img)
            while True:
                img_save=input('이대로 저장하겠습니까? (y / n) : ')
                if img_save=='y' or img_save=='Y' or img_save=='n' or img_save=='N':
                    break
                else:
                    print('y 혹은 n 을 입력해주세요.')
                    print()
                    continue
            if img_save=='n' or img_save=='N':
                print('시각화를 다시 시작합니다.')
                print()
                continue

            # 워드클라우드
            os.chdir('..\\')
            dir = os.getcwd()
            fpath=dir+'\\Font\\malgun.ttf'
            font=font_manager.FontProperties(fname=fpath).get_name()
            rc('font',family=font)

            wc=WordCloud(font_path=fpath,background_color='white')
            cloud=wc.generate_from_text(kakao)
            cloud.to_file(kakao_img)
            cloud=wc.generate_from_text(insta)
            cloud.to_file(insta_img) 

            print()
            print('시각화를 완료했습니다.')
            break



    #프로그램 종료--------------------------------------------------------------------------------------------------------
    print()
    print('프로그램을 종료합니다.')
    break
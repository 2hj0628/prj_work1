1. Web_driver 위치 확인

	1-1) Team2_Project1_Result(ver1.0)\Project_code 하위에 Web_driver 폴더가 있는지 확인

2. Font 위치 확인

	2-1) Team2_Project1_Result(ver1.0)\Project_code 하위에 Font 폴더가 있는지 확인

3. 비쥬얼 스튜디오, 파이선 설치 

	3-1) Team2_Project1_Result(ver1.0)\Environment 속의 VSCodeUserSetup-x64-1.69.2.exe 실행하여 비쥬얼 스튜디오 설치

	3-2) Team2_Project1_Result(ver1.0)\Environment 속의 python-3.10.6-amd64.exe 실행하여 파이썬 설치

4. 코드 실행하기
	
	4-1) 비쥬얼 스튜디오 실행

	4-2) Team2_Project1_Result(ver1.0)\Project_code 폴더 열기

	4-3) project_last_final.py 클릭

5. 터미널창 띄우기 (  '->' 이후 글자만 입력)
	
	5-1) 보기 탭에서 터미널 클릭

	5-2) 화면 하단에 생긴 터미널창의 빈 네모박스 클릭

	5-3) virtualenv 모듈 설치 (프로그램을 처음으로 실행 할 경우 한번만 입력합니다.) 

		-> pip install virtualenv 입력


	5-4) virtualenv 모듈이 정상적으로 설치 되었다면 가상환경 구현 (프로그램을 처음으로 실행 할 경우 한번만 입력합니다.) 

		-> virtualenv venv --python=3.10.6 


	5-5) 가상환경 구동 (비쥬얼스튜디오를 종료 후 다시 실행 할 때 마다 입력합니다.)

		-> .\venv\Scripts\activate
		*** 오류 발생 시 8-1번 참고

6. 인터프리터 설정

	6-1) ctrl+shift+P 누르기
		
	6-2) 화면 상단의 Python 3.10.6('venv':venv) 선택

	6-3) 화면 우측 하단의 파란 줄에서 3.10.6('venv':venv) 출력 확인.

7. 모듈 설치 

	-> pip install -r piplist.txt
	*** 오류 발생 시 8-3번 참고

8. 오류 발생 (콘솔창에 입력)

	8-1) 가상환경 구동 중 권한 오류 발생시
		-> Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
		또는 -> Set-ExecutionPolicy Unrestricted

	8-2) 8-1로 설정해도, 스크립트 실행 여부를 확인할 때
		-> Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope CurrentUser

	8-3) 모듈 설치중 fatal error 오류 발생시
		-> python -m pip install -r piplist.txt





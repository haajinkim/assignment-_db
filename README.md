# 서버 실행 방법

1. 파이썬 버전은 3.9 입니다.
    pyenv 로 3.9버전으로 맞춰서 작업하였습니다. 
    
2. vscode 기준) assignment_db 폴더를 엽니다.

3. 터미널창에 `poetry install` 을 입력합니다
  #### poetry 가 깔려 있지 않은 경우
 `pip install poetry`   
 #### vscode interpreter 가 잡히지 않을경우 ->  
 `poetry config virtualenvs.in-project true`  
 `poetry config virtualenvs.path "./.venv"`  
 을 터미널에 실행한후 vscode 를 재시작하고 인터프리터 경로를 입력해주시면 됩니다.  
 입력후 `pip install poetry`
 ex) C:\Users\PC\Desktop\assignment_db\.venv\Scripts 에 위치한 python 파일 선택

 #### FileNotFoundError 에러 
 #### poetry 가 인식하지 않은 경우가 있습니다. .venv 파일을 삭제 한후 다시 진행 해주세요.

4. 서버실행 : 터미널창에 `poetry run python manage.py runserver` 을 입력합니다.

5. Database는 내장 splite3 을 사용하였으며, 서버실행시 자동으로 생성 됩니다.

6. test코드는 각 앱 tests 폴더에 있습니다.

7. test 실행 법 : `poetry run python manage.py test`


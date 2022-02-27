# 프로그램 사용 매뉴얼  

#### API 종류  

- 환자 정보 및 방문 통계  
- concept 관련 정보 검색  

총 2개의 엔드포인트로 구성되어 있으며,  
환자 정보는 전체 환자 수 및 성별, 인종 등 주어진 조건에 따라 표시됩니다.  
방문 통계 역시 방문 유형을 비롯해 조건에 따라 값을 반환합니다.  

### 실행 방법  

1. 로컬에서 가상환경을 설치 후 활성화합니다.  
(https://docs.conda.io/en/latest/miniconda.html)  

2. 저장소를 복제합니다.   
(git clone https://github.com/solarrrrr1010/lws)  

3. 서버 실행에 필요한 모듈들을 설치합니다.  
pip install -r requirements.txt  

4. manage.py 파일과 같은 경로에 my_settings.py를 생성 후  
DATABASES와 SECRET_KEY 정보를 넣어줍니다.  
SECRET_KEY는 이메일을 확인하시면 됩니다.  

5. 서버를 실행합니다.  
python manage.py runserver  

7. Postman을 통한 API 테스트를 진행합니다.  
[🔗️ API 명세](https://documenter.getpostman.com/view/18177245/UVkqrZtY)  

8. 서버를 종료합니다.  
control + C  

### DB 튜닝 방법
* 현재 eager_loading과 로컬 쿼리 캐시를 적용해 불필요한 쿼리를 줄이고  
정보 반환 속도를 향상시켰습니다.  

* DB 인덱싱, 필요한 곳에 적절한 캐싱, iterator() 사용 등이 있습니다.  

* 파티셔닝, 샤딩을 통해 성능 향상을 볼 수 있습니다.  

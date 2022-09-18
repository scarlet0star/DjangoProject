# MyDjangoProjectCommunity
python-version: 3.8.13

## 한국의 커뮤니티 사이트를 클론 코딩한 프로젝트 MyCommunity
Django로 구현한 간단한 커뮤니티 사이트입니다. 커뮤니티 사이트들을 참고하여 비슷한 기능을 하도록 구현했으며, AWS EC2 Ubuntu 20.04 환경에서 Docker-compose를 통해 서비스할 수 있었습니다.

### 개발 기간
2022/07/01 ~ 2022/09/13

### 기술 스택
* Python Django
* NGINX
* MYSQL
* Docker, Docker-Compose
* AWS EC2
* etc
    * Gunicorn
    * Summernote
    * Bootstrap

### 설명
MyCommunity는 사용자 정보의 userinfo와 게시판과 게시글, 댓글을 다루는 board 두 가지의 앱으로 구성되어있습니다. 

userinfo는 Django에서 권장하는 대로 Django contrib의 Auth를 사용했으며, AbstractUser Model를 상속받아 User 정보를 생성하고 로그인/로그아웃과 CRUD 4가지 기능을 지원합니다.

board는 게시판과 게시글, 댓글의 모델이 정의되어 있습니다. 게시판은 생성과 조회를 지원하며, 게시글과 댓글은 CRUD 4가지 기능을 모두 지원합니다. 게시판의 게시글들은 페이징 처리되어 있으며 검색이 가능합니다.

### 구성
 * models.py : 앱에서 사용하는 모델들을 정의했고, MYSQL을 통해서 생성됩니다.
 * views.py : View는 거의 대부분 Class 형태로 구성되었습니다.
 * urls.py : URLconf
 * form.py : models.py에서 생성된 모델을 이용하여 자동적으로 form을 생성합니다.
 * /templates : views.py와 urls.py를 통해 만들어진 웹페이지에 출력되는 html들 입니다.  
 * /MyCommunity/settings.py(for github) : 프로젝트 보안을 위한 내용을 제외한 프로젝트 세팅입니다.
  
### 그 외
사이트 UI는 bootstrap을 이용하여 구성하였습니다. 아직 Ajax를 통한 비동기처리는 지원하지 않으며, 모바일 웹을 고려하여 디자인이 수정되지 않았습니다. 또한 github 기록은 프로젝트 보안과 관련된 파일의 업로드로 인해서 초기화 되었습니다.
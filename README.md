# SoundHub

`SoundHub` 는 여러 뮤지션들이 각자의 음악을 서로 공유할 수 있는 플랫폼 서비스입니다. 각자의 창작물을 공유하는 것에서 더 나아가 서로의 음악에 컨트리뷰트 할 수 있는 서비스를 제공합니다.  

[SoundHub](https://soundhub.che1.co.kr/)  

- - -

### 스펙

- 웹 서버: Nginx
- WSGI: uWGSI
- 어플리케이션: 
    - Django 1.11
    - Python 3.6.3
    - REST framework
    - Celery
- 저장소: AWS S3
- 데이터베이스: AWS RDS Postgresql
- 배포: 
    - AWS Elasticbeanstalk
    - Docker 
- Required package:
    - libav-tools
    - libavcodec-ffmpeg-extra56
    

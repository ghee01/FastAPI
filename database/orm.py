# database/orm.py
#   - 역할 : 모든 ORM 모델(테이블 클래스)의 부모가 되는 Base 클래스 정의
# 
# ORM(Object Relational Mapping)
#   - SQL을 직접 작성하지 않고, python 클래스로 DB 테이블을 다루는 방식
#   - ex) Todo 클래스 --> todo 테이블 자동 생성

from sqlalchemy.orm import DeclarativeBase
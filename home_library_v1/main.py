'''
home_library_v1/main.py

Version 3 - ISBN 추출

예광탄 방식을 활용한 아주 얇은 코드
'''

from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Book
from services.recognition import lookup_metadata, normalize_isbn

UPLOAD_DIR = Path('uploads')
UPLOAD_DIR.mkdir(exist_ok=True)

# models.py에서 정의한 Book, ReadingStatus, Review 클래스들을 실제 PostgreSQL 테이블로 생성하는 역할
# 이미 테이블이 있으면 넘어가고, 없으면 새로 만든다
Base.metadata.create_all(engine)

# FastAPI 앱 객체 생성, title → /docs(스웨거 문서)에서 화면 상단에 표시될 이름
app = FastAPI(title='우리집 책장 API')

# ---------------------------------------------------------------
# GET /books/lookup → ISBN 문자열만으로 책 정보를 바로 조회하는 API
# ---------------------------------------------------------------
@app.get('/books/lookup')
def lookup_book(isbn: str, db: Session = Depends(get_db)):
    validated_isbn = normalize_isbn(isbn)

    if not validated_isbn:
        raise HTTPException(422, '유효한 ISBN 형식이 아닙니다.')

    existing_book = db.scalar(select(Book).where(Book.isbn == validated_isbn))
    if existing_book:
        raise HTTPException(
            409,
            f'이미 등록된 책입니다: {existing_book.title} (id={existing_book.id})',
        )

    metadata = lookup_metadata(validated_isbn)

    if not metadata:
        raise HTTPException(404, '조회된 서지정보가 없습니다.')

    book = Book(
        title=metadata['title'],
        isbn=metadata['isbn'],
        author=metadata['author'],
        publisher=metadata['publisher'],
        cover_path=None,
        recognition_status='confirmed',
    )

    db.add(book)
    db.commit()
    db.refresh(book)

    return book

# ----------------------------------------------------
# GET /books → 등록된 책 전체 목록을 돌려주는 API
# ----------------------------------------------------
@app.get('/books')
def list_books(db: Session = Depends(get_db)):
    # select(Book) → Book 테이블에서 모두 가져와라. SQL SELECT문을 파이썬 코드로 작성
    # db.scalars(...).all() → SELECT문을 실제로 DB에 실행시키고 결과를 파이썬 리스트로 받는다
    return db.scalars(select(Book)).all()


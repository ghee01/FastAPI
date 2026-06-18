from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/blogdb'

engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    bind=engine
)
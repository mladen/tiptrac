import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# from databases import Database


# Gets the DATABASE_URL, MYSQL_USER and MYSQL_PASSWORD from environment variables
DATABASE_URL = os.environ["DATABASE_URL"]
# MYSQL_USER = os.environ["MYSQL_USER"]
# MYSQL_PASSWORD = os.environ["MYSQL_PASSWORD"]

print(DATABASE_URL)
# Builds the DATABASE_URL for SQLAlchemy
# SQLALCHEMY_DATABASE_URL = DATABASE_URL.format(
#     user=MYSQL_USER, password=MYSQL_PASSWORD, database="tiptracdb"
# )
# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://${MYSQL_USER}:${MYSQL_PASSWORD}@db/tiptracdb"
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Sets up SQLAlchemy's engine and session
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_size=20,
    max_overflow=0,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# The base for SQLAlchemy ORM models
Base = declarative_base()

# Asynchronous database support
# database = Database(SQLALCHEMY_DATABASE_URL)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from dotenv import load_dotenv

# load .env
load_dotenv(dotenv_path="config/.env", verbose=True)

host = os.environ.get('host')
port = os.environ.get('port')
user = os.environ.get('user')
password = os.environ.get('password')
db = os.environ.get('db')
dbtype = os.environ.get('dbtype')

# SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root1234@localhost:3306/boilerplate" 
SQLALCHEMY_DATABASE_URL = f"{dbtype}://{user}:{password }@{host}:{port}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQL_ALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db"
SQL_ALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:3306/TodoApplicationDatabase"

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)#, connect_args={"check_same_thread":False})

SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind=engine)

Base = declarative_base()


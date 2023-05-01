from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import settings

engine = create_engine(settings.SQLALCHEMY_DB_URL)
MetaData().create_all(engine)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)
Base = declarative_base()

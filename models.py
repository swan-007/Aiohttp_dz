import os

from dotenv import load_dotenv
from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String, Text,
                        func)
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm.session import sessionmaker

load_dotenv()

PG_DSN = (
    f"postgresql+asyncpg://{os.getenv('db_user')}:{os.getenv('db_password')}@"
    f"{os.getenv('db_host')}:{os.getenv('db_port')}/{os.getenv('db_name')}"
)
engine = create_async_engine(PG_DSN)
Base = declarative_base()
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    password = Column(String(60), nullable=False)
    time = Column(DateTime, server_default=func.now())



class Advertisement(Base):
    __tablename__ = "advertisements"

    id = Column(Integer, primary_key=True)
    heading = Column(String(20), nullable=False)
    description = Column(Text)
    date_of_creation = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User", backref="advertisements")





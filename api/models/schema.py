from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Define the base model for creating tables
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    userid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    # One-to-Many relationship: A user can save many articles
    articles = relationship("Article", back_populates="user")


class Article(Base):
    __tablename__ = "articles"
    articleid = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String)
    extract = Column(String)
    keyword = Column(String)
    tags = Column(String) # Store tags as a comma-separated string
    user_id = Column(Integer, ForeignKey("users.userid"))

    # One-to-Many relationship with User
    user = relationship("User", back_populates="articles")



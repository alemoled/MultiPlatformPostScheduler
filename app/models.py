from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

post_accounts = Table(
    "post_accounts", Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("account_id", ForeignKey("social_accounts.id"), primary_key=True),
)
class SocialAccount(Base):
    __tablename__ = "social_accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    platform = Column(String)  # e.g., 'twitter', 'facebook'
    account_name = Column(String)  # e.g., "@carenthusiast"
    access_token = Column(String)
    refresh_token = Column(String, nullable=True)
    extra_data = Column(Text)  # For storing JSON like profile info or IDs

    user = relationship("User", back_populates="accounts")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)

    accounts = relationship("SocialAccount", back_populates="user")
    posts = relationship("Post", back_populates="user")



class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    title = Column(String)
    description = Column(Text)
    image_url = Column(String)
    platforms = Column(String)  # comma-separated list
    schedule_time = Column(DateTime)
    status = Column(String, default="pending")  # pending, posted, failed

    user = relationship("User", back_populates="posts")
    logs = relationship("PostLog", back_populates="post")
    accounts = relationship("SocialAccount", secondary=post_accounts)



class PostLog(Base):
    __tablename__ = "post_logs"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    platform = Column(String)
    success = Column(Boolean)
    response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="logs")

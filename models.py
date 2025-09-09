
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os, uuid

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    conversations = relationship('Conversation', back_populates='user')
    documents = relationship('Document', back_populates='user')

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship('User', back_populates='conversations')
    messages = relationship('Message', back_populates='conversation')

class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey('conversations.id'))
    role = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    conversation = relationship('Conversation', back_populates='messages')

class Document(Base):
    __tablename__ = 'documents'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    filename = Column(String)
    storage_path = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)
    user = relationship('User', back_populates='documents')

def get_engine():
    database_url = os.getenv('DATABASE_URL', 'sqlite:///./medical.db')
    return create_engine(database_url, connect_args={ 'check_same_thread': False } if database_url.startswith('sqlite') else {})

def create_tables():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

def get_session_local():
    engine = get_engine()
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

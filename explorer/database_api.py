from sqlalchemy import (
    create_engine,
    String,
    Integer,
    Column,
)

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)

from sqlalchemy.ext.declarative import declarative_base

from decouple import config

DATABASE_URL = config("DATABASE_URL")


ENGINE = create_engine(DATABASE_URL, echo=True)
session_factory = sessionmaker(bind=ENGINE)
SESSION = scoped_session(session_factory)
BASE = declarative_base()

class ScannedChat(BASE):
	__tablename__ = "scanned_chat"
	chat_id = Column(Integer(20), primary_key = True)
	chat_title = Column(String(50))
	chat_hash = Column(String(50))
	last_scanned_message_id = Column(String(20))
    got_invite_from = Column(Integer(20))
    total_invites_found = Column(Integer(20))
    
	def __init__(
		self,
		chat_id,
		chat_title,
		last_scanned_message_id = None,
		got_invite_from = None,
        ):
        	self.chat_id = chat_id
        	self.chat_title = chat_title
        	self.last_scanned_message_id = last_scanned_message_id
        	self.got_invite_from = got_invite_from
        	self.total_invites_found = 0

async def add_new_chat(chat_id, chat_title, got_invite_from = None):
	chat = ScannedChat(
		chat_id,
		chat_title,
		got_invite_from,
     	)
    SESSION.add(chat)
    SESSION.commit()

async def set_last_scanned(chat_id, last_scanned_message_id):
	chat = SESSION.query(ScannedChat).get(chat_id)
	chat.last_scanned_message_id = last_scanned_message_id
	SESSION.commit()

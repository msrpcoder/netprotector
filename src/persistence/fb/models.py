from __future__ import annotations
from sqlalchemy import Column, String, Date
from sqlalchemy.orm import Session
from typing import Union
from .base import Base, engine


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False, index=True)
    last_profile_sync = Column(Date, nullable=True, index=True)
    last_friends_sync = Column(Date, nullable=True, index=True)
    last_posts_sync = Column(Date, nullable=True, index=True)

    @staticmethod
    def get_by_id(profile_id: str, session: Session = None) -> Union[Profile, None]:
        if not session:
            session = Session(engine)

        with session.begin():
            profile_dtls = session.query(Profile).filter(id == profile_id).first()

        return profile_dtls

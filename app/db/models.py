import enum
import sqlalchemy

from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .session import Base

class UserRole(
    enum.Enum,
):
    client = 'client'
    admin = 'admin'

class User(Base):
    __tablename__ = 'users'
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    full_name = Column(
        String,
        nullable=False,
    )
    email = Column(
        String,
        nullable=False,
        unique=True,
    )
    password = Column(
        String,
        nullable=False,
    )
    phone_number = Column(
        String,
        nullable=False,
        unique=True,
    )
    role = Column(
        sqlalchemy.Enum(UserRole),
        nullable=False,
        default=UserRole.client,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('now()'),
    )
    
    events = relationship(
        argument='Event',
        secondary='event_owners',
        back_populates='owners',
    )
    
class Event(Base):
    __tablename__ = 'events'
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    title = Column(
        String,
        nullable=False,
    )
    date = Column(
        DateTime(timezone=False),
        nullable=False,
    )
    location = Column(
        String,
        nullable=False,
    )
    photo_path = Column(
        String,
        nullable=True,
    )
    custom_message = Column(
        String,
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('now()'),
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=sqlalchemy.func.now(),
    )
    created_by = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    updated_by = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=True,
    )
    
    owners = relationship(
        argument='User',
        secondary='event_owners',
        back_populates='events',
    )
    guests = relationship('Guest', back_populates='event')


class Event_Owners(Base):
    __tablename__ = 'event_owners'
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    event_id = Column(
        Integer,
        ForeignKey('events.id'),
        nullable=False
    )
    user_id = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False
    )
    added_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('now()'),
    )

class GuestStatus(
    enum.Enum,
):
    invited = 'invited'
    accepted = 'accepted'
    declined = 'declined'
    maybe = 'maybe'
    no_response = 'no_response'

class Guest(
    Base,
):
    __tablename__ = 'guests'
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
    )
    event_id = Column(
        Integer,
        ForeignKey('events.id'),
        nullable=False,
    )
    full_name = Column(
        String,
        nullable=False,
    )
    phone_number = Column(
        String,
        nullable=False,
    )
    status = Column(
        sqlalchemy.Enum(GuestStatus),
        nullable=False,
        server_default=GuestStatus.no_response.value,
    )
    num_of_guests = Column(
        Integer,
        nullable=True,
        default=1
    )
    guest_update_time = Column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=text('now()'),
    )
    created_by = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        nullable=True,
        onupdate=sqlalchemy.func.now(),
    )
    updated_by = Column(
        Integer,
        ForeignKey('users.id'),
        nullable=True,
    )
    event = relationship(
        Event,
        back_populates='guests'
    )
    created_by_user = relationship(
        User,
        foreign_keys=[created_by]
    )
    updated_by_user = relationship(
        User,
        foreign_keys=[updated_by]
    )


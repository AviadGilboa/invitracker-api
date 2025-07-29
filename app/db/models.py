import enum
import sqlalchemy

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .session import Base

class UserRole(
    enum.Enum
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
        unique=False,
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
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text('now()'),
    )
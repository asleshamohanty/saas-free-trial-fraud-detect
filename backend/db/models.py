from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Fingerprint(Base):
    __tablename__ = "fingerprints"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    hash = Column(String, index=True)


class SignupEvent(Base):
    __tablename__ = "signup_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    fingerprint_id = Column(UUID(as_uuid=True), ForeignKey("fingerprints.id"))
    ip_address = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    risk_score = Column(Integer, nullable=True)
    action = Column(String, nullable=True)
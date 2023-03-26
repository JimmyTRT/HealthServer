import uuid
import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Controller(Base):
    __tablename__ = 'controllers'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    created_at = Column(String)
    updated_at = Column(String)
    ip_wan = Column(String)
    ip_vpn = Column(String)
    port = Column(Integer)

    events = relationship("Event", back_populates="controller")
#    ipadressen = relationship("Ipadress", back_populates="controller")


class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    controller_id = Column(String, ForeignKey('controllers.id'), nullable=False)

    controller = relationship("Controller", back_populates="events")

class Ipadress(Base):
    __tablename__ = 'ipadressen'

    id = Column(String, primary_key=True)
    ip_adress = Column(String, nullable=False, unique=True)
    controller_id = Column(String, ForeignKey('controllers.id'))

 #   controller = relationship("Controller", back_populates="ipadressen")
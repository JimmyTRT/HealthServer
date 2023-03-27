from sqlalchemy import create_engine, Column, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.exc import SQLAlchemyError
import uuid
import datetime
from logger import setup_logger

logger = setup_logger()
engine = create_engine("sqlite:///health.db")
Base = declarative_base()


class Controller(Base):
    __tablename__ = "controllers"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String(10))

    events = relationship("Event", back_populates="controller")


class Event(Base):
    __tablename__ = "events"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    controller_id = Column(String, ForeignKey("controllers.id"))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    event_name = Column(String)
    event_status = Column(String)
    server_ok = Column(Boolean)

    controller = relationship("Controller", back_populates="events")


class Ip(Base):
    __tablename__ = "ip"

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    controller_id = Column(String, ForeignKey("controller.id"))
    ip_address = Column(String)

    controller = relationship("Controller", back_populates="ip_addresses")

    def __repr__(self):
        return f"Ip(id={self.id!r}, controller_id={self.controller_id!r}, ip_address={self.ip_address!r})"


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.create_tables()
        self.logger.info("Database geactiveerd")

    def create_tables(self):
        try:
            Base.metadata.create_all(engine)
        except SQLAlchemyError as e:
            print(e)

    def add_controller(self, name, ip, vpn):
        controller_id = str(uuid.uuid4())
        controller = Controller(id=controller_id, name=name, ip=ip, vpn=vpn)
        try:
            with engine.connect() as conn:
                conn.add(controller)
                conn.commit()
        except SQLAlchemyError as e:
            print(e)

        return controller_id

    def add_event(self, controller_id, event_name, event_status, server_ok):
        event_id = str(uuid.uuid4())
        event = Event(id=event_id, controller_id=controller_id, event_name=event_name, event_status=event_status,
                      server_ok=server_ok)
        try:
            with engine.connect() as conn:
                conn.add(event)
                conn.commit()
        except SQLAlchemyError as e:
            print(e)

        return event_id

    def print_controllers(self):
        with engine.connect() as conn:
            controllers = conn.execute(Controller.__table__.select())
            for controller in controllers:
                print(controller)

    def get_controllers(self):
        with engine.connect() as conn:
            controllers = conn.execute(Controller.__table__.select())
            return [dict(c) for c in controllers]

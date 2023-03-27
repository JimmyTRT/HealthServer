from sqlalchemy import create_engine, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedColumn, relationship
import sqlite3
import datetime
from sqlite3 import Error
import uuid
from logger import setup_logger

# Conversie van sqlite db naar een sqlalchemy opzet
# zodat het mogelijk is om te wisselen tussen sqlite op development naar productie postgresql

engine = create_engine("sqlite:///health.db")


class Base(DeclarativeBase):
    pass


class Controller(Base):
    __tablename__ = "controller"

    id: Mapped[str] = MappedColumn(primary_key=True)
    controller_name: Mapped[str] = MappedColumn(String(10))
    active: Mapped[bool] = MappedColumn()

    def __repr__(self) -> str:
        return f"controller(id={self.id!r}, controller naam={self.controller_name!r}, active={self.active!r})"

class Ip(Base):
    __tablename__ = "ip"

    id: Mapped[str] = MappedColumn(primary_key=True)
    controller_id: Mapped[str] = MappedColumn(ForeignKey("controller.id"))
    ip: Mapped[str] = MappedColumn[String(16)]

    def __repr__(self) -> str:
        return f"ip(id={self.id!r}, controller id={self.controller_id!r}, ip={self.ip!r})"

class event(Base):
    pass


class Database:
    def __init__(self, db_file):
        # create logger
        self.logger = setup_logger()
        self.db_file = db_file
        self.create_tables()
        self.logger.info("Database geactiveerd")

    def create_connection(self):
        conn = None
        try:
            self.logger.info(f"Connectie maken met {self.db_file}")
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

        return conn

    def create_tables(self):
        conn = self.create_connection()
        cursor = conn.cursor()

        # Create the controller table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS controllers
                            (id TEXT PRIMARY KEY,
                            name TEXT,
                            ip TEXT,
                            vpn TEXT)''')

        # Create the events table if it doesn't exist
        cursor.execute('''CREATE TABLE IF NOT EXISTS events
                            (id TEXT PRIMARY KEY,
                            controller_id TEXT,
                            timestamp TEXT,
                            event_name TEXT,
                            event_status TEXT,
                            server_ok TEXT,
                            FOREIGN KEY (controller_id) REFERENCES controllers(id))''')

        conn.commit()
        conn.close()

    # Genereer een willekeurige UUID
    # random_uuid = uuid.uuid4()
    def add_controller(self, name, ip, vpn):
        self.logger.info("add controller")
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO controllers (id, name, ip, vpn) VALUES (?, ?, ?, ?)",
                       (str(uuid.uuid4()), name, ip, vpn))
        conn.commit()

        controller_id = cursor.lastrowid
        conn.close()

        return controller_id

    def add_event(self, controller_id, timestamp, event_name, event_status, server_ok):
        conn = self.create_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO events (controller_id, timestamp, event_name, event_status, server_ok) VALUES (?, ?, ?, ?, ?)",
            (controller_id, datetime.datetime.now(), event_name, event_status, server_ok))
        conn.commit()

        event_id = cursor.lastrowid
        conn.close()

        return event_id

    def print_controllers(self):
        """Print alle controllers in de controllers tabel naar de console"""
        conn = self.create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM controllers")
            rows = cur.fetchall()
            for row in rows:
                print(row)

    def get_controllers(self):
        conn = self.create_connection()
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM controllers")
            return cur.fetchall()

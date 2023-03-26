from fastapi import FastAPI
from logger import setup_logger
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from ..database import models, database

logger = setup_logger()
api = FastAPI()


@api.post('/write')
def write_data():
    # ontvang data van de server
    data = {'key': 'value'}
    logger.info(f'api write:' + data)
    # schrijf data weg naar de database
    #   conn = sqlite3.connect('database.db')
    #   cursor = conn.cursor()
    #   cursor.execute('INSERT INTO my_table (key, value) VALUES (?, ?)', (data['key'], data['value']))
    #   conn.commit()
    #   conn.close()
    return {'message': 'Data is weggeschreven naar de database.'}


# Model voor de JSON-payload
class EventCreate(BaseModel):
    controllernaam: str
    timestamp: str
    event: str
    value: float


# Endpoint om een nieuw event toe te voegen
@api.post("/events/")
async def create_event(event: EventCreate, db: Session = database.session):
    # JSON-payload in dictionary-object omzetten
    event_data = event.dict()

    # Nieuw Event object maken
    new_event = models.Event(**event_data, created_at=datetime.now())

    # Event object opslaan in de database
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    # Return response met de nieuwe event data
    return new_event

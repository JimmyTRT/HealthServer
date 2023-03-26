from fastapi import FastAPI
import logging

from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
#from ..database import models, database
import database.models

logger = logging.getLogger(__name__)
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


@api.post('/hello')
def api_hello(data: dict):
    """
    De eerste melding van een controller.

    Bewaren van de gegevens in de database.
    Indien de controller al bestaat
        * bij veranderde gegevens database update
        * bij onveranderde gegevens geen actie

    :param data: controllernaam, ip_wan, ip_vpn, poort

    :return: UUID van de aangemaakte controller
    """
    # ontvang data van de server

    logger.info(f"api write: controllernaam: {data.get('controllernaam')}, ip_wan: {data.get('ip_wan')},"
                f"ip_vpn: {data.get('ip_vpn')}, poort: {data.get('poort')} ")
    # Nazien of de controller al bestaat.
    print(f"FEEEEEEEEEESTTTTTTTTJEEEEEEEEEEEEEEEE {database.get_controller_exists(data.get('controllernaam'))}")
    print(database.get_controller_exists(data.get("controllernaam")))

    if database.get_controller_exists(data.get("controllernaam")):
        print("controller bestaat")
        #Data van de controller update indien niet gelijk en return UUID
        info = database.get_id_controller(data.get("controllernaam"))
        print(f"UUID van {data.get('controllernaam')} is {info}")
        return info
    else:
        #controller aanmaken
        database.add_controller(data.get('controllernaam'), data.get('ip_wan'), data.get('ip_vpn'), data.get('poort'))
    return {'UUID': database.get_id_controller(data.get('controllernaam'))}

# Model voor de JSON-payload
class EventCreate(BaseModel):
    controllernaam: str
    timestamp: str
    event: str
    value: float


# # Endpoint om een nieuw event toe te voegen
# @api.post("/events/")
# async def create_event(event: EventCreate, db: Session = database.session):
#     # JSON-payload in dictionary-object omzetten
#     event_data = event.dict()
#
#     # Nieuw Event object maken
#     new_event = models.Event(**event_data, created_at=datetime.now())
#
#     # Event object opslaan in de database
#     db.add(new_event)
#     db.commit()
#     db.refresh(new_event)
#
#     # Return response met de nieuwe event data
#     return new_event

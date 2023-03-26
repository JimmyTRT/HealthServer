import uuid

from . import utils
from . import models
from . import database
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


def add_controller(naam, ip1, ip2):
    controller = models.Controller(id=str(uuid.uuid4()), name=naam,
                                   created_at=str(datetime.now()), ip_wan=ip1, ip_vpn=ip2)
#    controller = models.Controller(name=naam,
#                                   created_at=str(datetime.now()), ip_wan=ip1, ip_vpn=ip2)
    utils.add_controller(controller)

def get_id_controller(naam):
    #todo: try catch toevoegen
    try:
        controller = database.session.query(models.Controller).filter(models.Controller.name==naam).first()
        print(controller.id)
        return controller.id
    except NoResultFound:
        return 'no result'
    except MultipleResultsFound:
        return 'To many result'




def show_controllers():
    controllers = database.session.query(models.Controller).all()
 #   controllers = utils.select_all(models.Controller)
    for controller in controllers:
        print(f"controllernaam: {controller.name}, {controller.id} met ip {controller.ip_wan} en vpn ip {controller.ip_vpn}")
#.strftime('%H:%M:%S.%f %d-%m-%Y')

def show_all():
    all_controllers = database.session.query(models.Controller).all()
    for controller in all_controllers:
        print(f"Controller ID: {controller.id}, Naam: {controller.name}")


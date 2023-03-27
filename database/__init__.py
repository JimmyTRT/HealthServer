import uuid
import logging
from . import utils
from . import models
from . import database
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


logger = logging.getLogger(__name__)


def add_controller(naam, ip1, ip2, poort):
    controller = models.Controller(id=str(uuid.uuid4()), name=naam,
                                   created_at=str(datetime.now()), ip_wan=ip1, ip_vpn=ip2, port=poort)
    utils.add_controller(controller)


def get_id_controller(naam):
    # todo: try catch toevoegen
    try:
        controller = database.session.query(models.Controller).filter(models.Controller.name == naam).first()
        logger.debug(f"get controller exists: {controller}")
        return controller
    except NoResultFound:
        return None
    except MultipleResultsFound:
        return None





def get_controller_exists(naam):
    """
    Kijken of een controller al bestaat in de database
    :param naam: naam van de controller
    :return: Boolean
    """
    try:
        controller = database.session.query(models.Controller).filter(models.Controller.name == naam).first()
        logger.info(f"get controller exists: {controller}")
        if controller is not None:
            return True
        else:
            return False
    except NoResultFound:
        return False
    except MultipleResultsFound:
        return False



def show_controllers():
    controllers = database.session.query(models.Controller).all()
    #   controllers = utils.select_all(models.Controller)
    for controller in controllers:
        print(
            f"controllernaam: {controller.name}, {controller.id} met ip {controller.ip_wan} en vpn ip {controller.ip_vpn}")


# .strftime('%H:%M:%S.%f %d-%m-%Y')

def show_all():
    all_controllers = database.session.query(models.Controller).all()
    for controller in all_controllers:
        print(f"Controller ID: {controller.id}, Naam: {controller.name}")


def get_controller_id_by_name(name):

    controller = database.session.query(models.Controller).filter_by(name=name).first()
    if controller:
        return controller.id
    else:
        return None

from .database import session
from .models import Controller, Event


# def add_controller(name, location, description):
#     controller = Controller(name=name, location=location, description=description)
#     session.add(controller)
#     session.commit()
#     return controller
#
#
# def add_event(name, description, start_time, end_time, controller_id):
#     event = Event(name=name, description=description, start_time=start_time, end_time=end_time, controller_id=controller_id)
#     session.add(event)
#     session.commit()
#     return event

def add_controller(controller):
    session.add(controller)
    session.commit()


def add_event(event):
    session.add(event)
    session.commit()


def add_ip(ip):
    session.add(ip)
    session.commit()

def select_all(data):
    returndata = session.query(data).all()
    session.commit()
    return returndata

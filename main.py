import uvicorn as uvicorn
import time
import threading
from www import app
from api import api
from schedule import every, repeat, run_pending
from logger import setup_logger
from database import engine
import database

# create logger
logger = setup_logger()

db = database.Database('health.db')




@repeat(every(10).seconds)
def job():
    logger.info('Run Job')


@repeat(every(1).minute)
def check_something():
    ctrl_id = db.add_controller('controller', '0.0.0.0', '1.1.1.1')
    logger.info(f'toevoegen controller {ctrl_id}')
    db.print_controllers()


def schedule():
    # lees waarde vanuit bestand elke 20 seconden
    while True:
        run_pending()
        time.sleep(1)


def check_calendar():
    # controleer de kalender elke minuut
    while True:
        logger.info("calendar")
        time.sleep(60)


def fast_api():
    uvicorn.run(api, host="0.0.0.0", port=9090)

#todo: Poort numers variable maken


# start de applicatie
if __name__ == '__main__':
    logger.info("Starting application")
    # start routine 1 - Flask applicatie
    logger.info("Starting www on port 8080")
    threads = []
    t_app = threading.Thread(target=app.run, kwargs={'port': 8080}).start()
    threads.append(t_app)
    # start routine 2 - FastAPI applicatie
    logger.info("Starting api on port 9090")
    t_api = threading.Thread(target=fast_api).start()
    threads.append(t_api)
    # start routine 3 - leest en schrijft data naar de database en voert tijdgebonden functies uit
    threading.Thread(target=schedule).start()
    threading.Thread(target=check_calendar).start()
    if threading.Thread(target=fast_api).is_alive():
        print("FastAPI thread is actief")

    if threading.Thread(target=schedule).is_alive():
        print("Schedule thread is actief")

    if threading.Thread(target=check_calendar).is_alive():
        print("Check calendar thread is actief")

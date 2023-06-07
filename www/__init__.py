from flask import Flask
from logger import setup_logger
import database

logger = setup_logger()
app = Flask(__name__)

#db = database.Database("health.db")

@app.route('/1')
def hello():
    return 'Hello, World!'

@app.route('/')
def lijst_controllers():
    logger.info("Flask show controllerlijst")
    # Lijst met controllers uit de database

    controllers = database.show_controllers()
    logger.info(controllers)
    # HTML-code voor het weergeven van de lijst als een tabel
    html = "<table>"
    html += "<tr><th width='10%'>ID</th width='400%'><th>Naam</th><th width='25%'>IP-adres</th><th width='25%'>VPN-adres</th></tr>"
    for controller in controllers:
        html += "<tr>"
        html += "<td width='10%'>{}</td>".format(controller.name)
        html += "<td width='40%'>{}</td>".format(controller.id)
        html += "<td width='25%'>{}</td>".format(controller.ip_vpn)
        html += "<td width='25%'>{}</td>".format(controller.ip_wan)
        html += "</tr>"
    html += "</table>"

    # Return HTML als response
    return html




def www_start():
    app.run(host='127.0.0.1',port=8080,debug=True)


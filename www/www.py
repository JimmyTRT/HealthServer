from flask import Flask

import database

app = Flask(__name__)


print('load database website')
@app.route('/1')
def hello():
    return 'Hello, World!'

@app.route('/')
def lijst_controllers():
    # Lijst met controllers uit de database
    controllers = database.show_controllers()

    # HTML-code voor het weergeven van de lijst als een tabel
    html = "<table>"
    html += "<tr><th>ID</th><th>Naam</th><th>IP-adres</th><th>VPN-adres</th></tr>"
    for controller in controllers:
        html += "<tr>"
        html += "<td>{}</td>".format(controller.name)
        html += "<td>{}</td>".format(controller.id)
        html += "<td>{}</td>".format(controller[2])
        html += "<td>{}</td>".format(controller[3])
        html += "</tr>"
    html += "</table>"

    # Return HTML als response
    return html




def www_start():
    app.run(host='127.0.0.1',port=8080,debug=True)


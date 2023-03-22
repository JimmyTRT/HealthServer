from fastapi import FastAPI

api = FastAPI()


@api.post('/write')
def write_data():
    # ontvang data van de server
    data = {'key': 'value'}
    # schrijf data weg naar de database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO my_table (key, value) VALUES (?, ?)', (data['key'], data['value']))
    conn.commit()
    conn.close()
    return {'message': 'Data is weggeschreven naar de database.'}

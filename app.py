from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
import requests, time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    tel = request.form.get('From')
    resp = MessagingResponse()

    #Si el mensaje incluye la palabra "pronostico"
    if "pronostico" in msg or "pronóstico" in msg.lower():
        url = 'http://api.openweathermap.org/data/2.5/forecast?q=Bogota&appid=4b912705f55a6cded8314651f6f124f5&units=metric'
        datos_clima = requests.get(url).json()

        for i in range(5):
            hora = time.strftime('%H', time.gmtime(datos_clima['list'][i]['dt']))
            horaInt = int(hora)
            horaCol = " "

            if horaInt-5 < 0:
                horaCol = str((12+horaInt)-5) + ":00 pm"
            else:
                if horaInt-5 < 12:
                    horaCol = str(horaInt-5) + ':00 am'
                elif horaInt-5 == 12:
                    horaCol = str(horaInt-5) + ':00 m'
                else:
                    horaCol = str((horaInt-5)-12) + ':00 pm'

            resp.message("Alrededor de las {} se espera {}".format(horaCol, datos_clima['list'][i]['weather'][0]['main']))

            time.sleep(0.5)
    else:
        #respuesta de DialogFlow
        respuesta = fetch_reply(msg, tel)

        #Crea la respuesta al usuario
        #resp = MessagingResponse()
        resp.message(respuesta)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

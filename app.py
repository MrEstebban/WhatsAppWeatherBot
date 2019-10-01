from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
from utils import dame_el_pronostico
import request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hey! My 'master' is Esteban Pedraza :D"

@app.route("/sms", methods=['POST'])
def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Fetch the message
    msg = request.form.get('Body')
    tel = request.form.get('From')
    resp = MessagingResponse()

    mensajeRecibido = msg.lower().strip()
    pronostico = " "

    #Si el ensaje incluye la palabra "pronostico"
    if "pronostico" in mensajeRecibido or "pronóstico" in mensajeRecibido:
        if mensajeRecibido == "pronóstico" or mensajeRecibido == "pronostico":
            url = 'http://api.openweathermap.org/data/2.5/forecast?q=Bogota,co&appid=4b912705f55a6cded8314651f6f124f5&units=metric&lang=es'
            datos_clima = requests.get(url).json()
            pronostico = "El pronóstico para Bogotá es:\n\n" + dame_el_pronostico(datos_clima)
        else:
            cadenaInvertida = mensajeRecibido[::-1]
            indice = 0
            for x in cadenaInvertida:
                if x == ' ':
                    break
                indice+=1

            pos = (len(mensajeRecibido)-1) - indice
            ciudad = mensajeRecibido[pos:].strip()
            #resp.message("ciudad:---{}---".format(ciudad))
            url = 'http://api.openweathermap.org/data/2.5/forecast?q={},co&appid=4b912705f55a6cded8314651f6f124f5&units=metric&lang=es'.format(ciudad)
            if str(requests.get(url)) == "<Response [200]>":
                datos_clima = requests.get(url).json()
                pronostico = "El pronóstico para {} es:\n\n".format(ciudad)
                pronostico += dame_el_pronostico(datos_clima)
                    #Fin for loop
            else:
                pronostico = "\U0001F613 No encontré la ciudad \"{}\", intenta enviando: Pronostico nombreTuCiudad".format(ciudad)
        resp.message(pronostico)

    else:
        #respuesta de DialogFlow
        respuesta = fetch_reply(msg, tel)
        #Crea la respuesta al usuario
        resp.message(respuesta)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

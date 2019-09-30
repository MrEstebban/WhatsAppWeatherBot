from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils import fetch_reply
from utils import dame_la_hora
import requests, time

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hey! My 'master' is Esteban Pedraza :D!"

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
            pronostico = "El pronóstico para Bogotá es:\n"

            for i in range(5):
                hora = time.strftime('%H', time.gmtime(datos_clima['list'][i]['dt']))
                horaInt = int(hora)
                horaCol = dame_la_hora(horaInt)
                desc_princ = datos_clima['list'][i]['weather'][0]['main']
                icono = " "
                if desc_princ == "Thunderstorm":
                    icono = "\U000026C8"
                elif desc_princ == "Drizzle" or desc_princ == "Rain":
                    icono = "\U0001F327"
                elif desc_princ == "Clear":
                    icono = "\U00002600"
                elif desc_princ == "Clouds":
                    icono = "\U000026C5"

                pronostico += "-A las {} se espera {} {}\n".format(horaCol, datos_clima['list'][i]['weather'][0]['description'], icono)
                #Fin for loop
        else:
            cadenaInvertida = mensajeRecibido[::-1]
            indice = 0
            for x in cadenaInvertida:
                if x == ' ':
                    break
                indice+=1

            pos = (len(mensajeRecibido)-1) - indice
            ciudad = mensajeRecibido[pos:]
            url = 'http://api.openweathermap.org/data/2.5/forecast?q={},co&appid=4b912705f55a6cded8314651f6f124f5&units=metric&lang=es'.format(ciudad)
            if str(requests.get(url)) == "<Response [200]>":
                datos_clima = requests.get(url).json()
                pronostico = "El pronóstico para {} es:\n".format(ciudad)

                for i in range(5):
                    hora = time.strftime('%H', time.gmtime(datos_clima['list'][i]['dt']))
                    horaInt = int(hora)
                    horaCol = dame_la_hora(horaInt)
                    desc_princ = datos_clima['list'][i]['weather'][0]['main']
                    icono = " "
                    if desc_princ == "Thunderstorm":
                        icono = "\U000026C8"
                    elif desc_princ == "Drizzle" or desc_princ == "Rain":
                        icono = "\U0001F327"
                    elif desc_princ == "Clear":
                        icono = "\U00002600"
                    elif desc_princ == "Clouds":
                        icono = "\U000026C5"

                    pronostico += "-A las {} se espera {} {}\n".format(horaCol, datos_clima['list'][i]['weather'][0]['description'], icono)
                    #Fin for loop
            else:
                pronostico = "No hemos encontrado la ciudad '{}', intenta enviando el mensaje 'Pronostico nombreTuCiudad'".format(ciudad)
        resp.message(pronostico)
        resp.message("Lo que enviaste: {}".format(mensajeRecibido))

    else:
        #respuesta de DialogFlow
        respuesta = fetch_reply(msg, tel)

        #Crea la respuesta al usuario
        #resp = MessagingResponse()
        resp.message(respuesta)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)

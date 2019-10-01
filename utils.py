import os, time
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "experimentowpp-vdaiew-9fd044d5158b.json"

import dialogflow_v2 as dialogflow
dialogflow_session_client = dialogflow.SessionsClient()
PROJECT_ID = "experimentowpp-vdaiew"

def detect_intent_from_text(text, session_id, language_code='es'):
    session = dialogflow_session_client.session_path(PROJECT_ID, session_id)
    text_input = dialogflow.types.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session, query_input=query_input)
    return response.query_result

def fetch_reply(query, session_id):
    response = detect_intent_from_text(query, session_id)
    return response.fulfillment_text

def dame_la_hora(horaInt):
    if horaInt-5 < 0:
        return str((12+horaInt)-5) + ":00 pm"
    else:
        if horaInt-5 < 12:
            return str(horaInt-5) + ':00 am'
        elif horaInt-5 == 12:
            return str(horaInt-5) + ':00 m'
        else:
            return str((horaInt-5)-12) + ':00 pm'

def dame_el_pronostico(datos_clima):
    pronostico = ""
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
    return pronostico

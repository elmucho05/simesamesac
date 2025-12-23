from flask import Flask, request
from flask_restful import Resource, Api

from prenotazione import Prenotazione
from prenotazione import RiepilogoGiorno
from prenotazione import RiunioneGiorno
from prenotazione import SlackerMese
from prenotazione import SabateurMese
from date_validation import *
import re


booking = Prenotazione()
riep = RiepilogoGiorno()
riunione_giorno = RiunioneGiorno()
slacker_mese = SlackerMese()
sabateur_mese = SabateurMese()

app = Flask(__name__, static_url_path="/static", static_folder="static")

api = Api(app)


basePath = "/api/v1"


class PrenotazioneResource(Resource):


    def post(self, date):
        prenotazione_ricevuta = request.json
        if date is None:
            return "Date is missing from URL. Format required: /room42/YYYY-MM-DD", 400
        if date_from_str(date) is None:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if prenotazione_ricevuta is None:
            return None, 400
        
        required_fields = ["colpevole", "vittime", "durata", "orario_inizio"]
        for field in required_fields:
            if field not in prenotazione_ricevuta:
                return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        colpevole = prenotazione_ricevuta["colpevole"]
        vittime = prenotazione_ricevuta["vittime"]
        durata = prenotazione_ricevuta["durata"]
        orario_inizio = prenotazione_ricevuta["orario_inizio"]

        if not isinstance(vittime, list):
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if len(vittime) > 20:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if not (0.5 <= durata <= 8):
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if durata % 0.5 != 0:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        time_pattern = re.compile(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$')
        if not time_pattern.match(orario_inizio):
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if time_from_str(orario_inizio).hour<8 or time_from_str(orario_inizio).hour > 19 :
           return "Conflitto di orario (sovrapposizione, inizio non valido o termine dopo le 20:00)", 422
        lista_riunioni = riunione_giorno.get_riunione_giorno(date) 
        if colpevole in lista_riunioni:
            return "Conflitto nella richiesta (duplicazione)", 409

        if check_sovrapposizione(lista_riunioni,orario_inizio, durata):
            return "Conflitto di orario (sovrapposizione, inizio non valido o termine dopo le 20:00)", 422
        booking_id = booking.create_prenotazione(
            date, colpevole, vittime, durata, orario_inizio
        )

        # Return the created object structure
        response_payload = {
            "data": date,
            "colpevole": colpevole,
            "vittime": vittime,
            "durata": durata,
            "orario_inizio": orario_inizio
        }
        return response_payload, 201
    def put(self, date):
        prenotazione_ricevuta = request.json
        if date is None:
            return "Date is missing from URL. Format required: /room42/YYYY-MM-DD", 400
        if date_from_str(date) is None:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if not prenotazione_ricevuta:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        
        required_fields = ["colpevole", "vittime", "durata", "orario_inizio"]
        for field in required_fields:
            if field not in prenotazione_ricevuta:
                return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        colpevole = prenotazione_ricevuta["colpevole"]
        vittime = prenotazione_ricevuta["vittime"]
        durata = prenotazione_ricevuta["durata"]
        orario_inizio = prenotazione_ricevuta["orario_inizio"]
        
        lista_riunioni = riunione_giorno.get_riunione_giorno(date) 
        if colpevole not in lista_riunioni :
            return "Prenotazione per data e colpevole specificati non trovata", 404
       
        if not isinstance(vittime, list):
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if len(vittime) > 20:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if not (0.5 <= durata <= 8):
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if durata % 0.5 != 0:
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        time_pattern = re.compile(r'^([0-1][0-9]|2[0-3]):[0-5][0-9]$')
        if not time_pattern.match(orario_inizio):
            return "Richiesta non valida (dati mancanti, data errata, troppi partecipanti, durata non valida, o colpevole già presente per quella data)", 400
        if time_from_str(orario_inizio).hour<8 or time_from_str(orario_inizio).hour > 19 :
             return "Conflitto di orario (sovrapposizione, inizio non valido o termine dopo le 20:00)", 422
        
        # stupid way for me to check sovvrapposizione
        # because if i check sovvrapposizione, of couse it's gonna say true
        # so i copy it to a new array, them delete that riunione so i can check if that colpevole has other meetings
        # and also if the new meeting data is "sovvrapposto"
        altre_riunioni = lista_riunioni.copy()
        
        if colpevole in altre_riunioni:
            del altre_riunioni[colpevole]

        if check_sovrapposizione(altre_riunioni,orario_inizio, durata):
            return "Conflitto di orario (sovrapposizione, inizio non valido o termine dopo le 20:00)", 422
        booking.create_prenotazione(
            date, colpevole, vittime, durata, orario_inizio
        )

        response_payload = {
            "data": date,
            "colpevole": colpevole,
            "vittime": vittime,
            "durata": durata,
            "orario_inizio": orario_inizio
        }
        return response_payload, 200


def check_sovrapposizione(lista_riunioni, start_time_str, duration):
    new_start = time_from_str(start_time_str)
    new_start_minutes = new_start.hour * 60 + new_start.minute
    new_end_minutes = new_start_minutes + int(duration * 60)

    day_end = 20 * 60
    if new_end_minutes > day_end:
        return True
    
    for meeting in lista_riunioni.values():
        existing_start = time_from_str(meeting["orario_inizio"])
        existing_start_minutes = existing_start.hour * 60 + existing_start.minute
        existing_duration = float(meeting["durata"])
        existing_end_minutes = existing_start_minutes + int(existing_duration* 60)
        if not (new_end_minutes <= existing_start_minutes or existing_end_minutes <= new_start_minutes):
            return True
    return False
class CleanDatabase(Resource):
    def post(self):
        booking.clean_database()
        return None, 200
class RiepilogoGiornoResource(Resource):

    def get(self, date):
        if(date is None): 
            return "Richiesta non valida", 400
        if(date_from_str(date) is None):
            return "Richiesta non valida", 400

        ret_val = riep.get_dettagli_giornata(date)
        if ret_val is None:
            return "Richiesta non valida", 400
        return ret_val, 200

class SlackerMeseResource(Resource):
    def get(self, mese):
        if mese is None:
            return "Richiesta non valida", 400
        if parse_month(mese) is None:
            return "Richiesta non valida", 400
         
        slacker = slacker_mese.get_slacker_mese(mese)
        if not slacker :
            return "Nessun dato disponibile per il mese specificato", 404
        return slacker, 200

class SabateurMeseResource(Resource):
    def get(self, mese):
        if mese is None:
            return "Richiesta non valida", 400
        if parse_month(mese) is None:
            return "Richiesta non valida", 400
        sabatuer = sabateur_mese.get_sabateur_mese(mese)
        if not sabatuer:
            return "Nessun dato disponibile per il mese specificato", 404
        
        return sabatuer,200
        

api.add_resource(
    PrenotazioneResource, f"{basePath}/room42/<string:date>"
) 
api.add_resource(RiepilogoGiornoResource, f"{basePath}/room42/<string:date>")
api.add_resource(CleanDatabase,f"{basePath}/panic")
api.add_resource(SlackerMeseResource, f"{basePath}/stats/slackers/<string:mese>")
api.add_resource(SabateurMeseResource, f"{basePath}/stats/saboteurs/<string:mese>")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)

from google.cloud import firestore
from date_validation import *


class Prenotazione(object):
    def __init__(self) -> None:
        self.db = firestore.Client()
    """
    La funzione di creazione la posso usare anche come di update SE
    aggiungiamo il tag : merge=True quando facciamo il set
    """
    def create_prenotazione(self, data, colpevole, vittime, durata, orario_inizio):
        doc_ref = self.db.collection("meeting_crimes").document(data)
        # unique_id = f"{data}_{orario_inizio}"
        #
        # doc_ref = self.db.collection("prenotazione").document(unique_id)
        #
        # payload = {
        #     "data": data,
        #     "colpevole": colpevole,
        #     "vittime": vittime,
        #     "durata": durata,
        #     "orario_inizio": orario_inizio,
        # }
        #
        # doc_ref.set(payload)
        #
        # print(f"Booking created: {unique_id}")
        
        booking_data = {
            colpevole: {
                "colpevole": colpevole,
                "orario_inizio": orario_inizio,
                "vittime": vittime,
                "durata": durata,
            }
        }
        doc_ref.set(booking_data, merge=True)
        print(f"Booking created for {data} at {orario_inizio}")
        return doc_ref.id
    def clean_database(self):
        doc_ref = self.db.collection("meeting_crimes")
        docs = doc_ref.list_documents()
        for doc in docs:
            print(f"Deleting doc {doc.id} => {doc.get().to_dict()}")
            doc.delete()




class RiunioneGiorno(object):
    def __init__(self):
        self.db = firestore.Client()

    def get_riunione_giorno(self, data):
        riunione = self.db.collection("meeting_crimes").document(data).get()
        if not riunione.exists:
            return {}
        return riunione.to_dict()

class RiepilogoGiorno(object):
    def __init__(self):
        self.db = firestore.Client()
        self.r_giorno = RiunioneGiorno()
    def get_dettagli_giornata(self, data):
        lista_riunioni = list(self.r_giorno.get_riunione_giorno(data).values())
        if lista_riunioni:
            totale_ore = sum(item["durata"] for item in lista_riunioni)
            meeting_piu_lungo = max(lista_riunioni, key=lambda x:x["durata"])
            dannato = meeting_piu_lungo["colpevole"]
            response = {
                "data": data,
                "totale_ore": totale_ore,
                "dannato_del_giorno": dannato,
                "riunioni": lista_riunioni,
            }
        else:
            response = {
                "data": data,
                "totale_ore": 0,
                "dannato_del_giorno": "",
                "riunioni" : []
            }
        return response

class RipilogoSettimana(object):
    def __init__(self):
        self.db = firestore.Client()
    
    def get_dettagli_settimana(self):
        pass
class SlackerMese(object):
    def __init__(self):
        self.db = firestore.Client()
        self.r_giorno = RiunioneGiorno()
    def get_monthly_totals(self, mese):
        month = parse_month(mese)
        if month is None:
            return None
        meetings_ref = self.db.collection("meeting_crimes")
        meeting_mensili = []
        for v in meetings_ref.get():
            print(v.id)
            if mese in v.id:
                meeting_mensili.append(v.id) 
        totals = {}
        for m in meeting_mensili:
            lista = self.r_giorno.get_riunione_giorno(m)
            for l in lista.values():
                duration = float(l["durata"])
                colpevole = l["colpevole"]
                if colpevole in totals:
                    totals[colpevole] +=duration
                else:
                    totals[colpevole] = duration
                
                vittime = l["vittime"]
                if vittime:
                    for v in vittime:
                        totals[v] = totals.get(v, 0) + duration
        if not totals: 
            return {}
        return totals

    def get_slacker_mese(self, mese):
        if not totals:
            return None

        totals = self.get_monthly_totals(mese)
        peggiore = max(totals, key= lambda x:totals[x])
        totale_ore_perse = totals[peggiore]
        efficienza = float(totale_ore_perse // 160)#160 ore menisili, 8h giorno per 5 giorni
        response = {
            "dipendente" : peggiore,
            "ore_riunion": totale_ore_perse,
            "efficienza" : efficienza
        }
        return response

class SabateurMese(object):
    def __init__(self):
        self.db = firestore.Client()
        self.r_giorno = RiunioneGiorno()
    def get_monthly_totals(self, mese):
        month = parse_month(mese)
        if month is None:
            return None
        meetings_ref = self.db.collection("meeting_crimes")
        meeting_mensili = []
        for v in meetings_ref.get():
            print(v.id)
            if mese in v.id:
                meeting_mensili.append(v.id) 
        totals = {}
        numero_vittime = 0
        totale_sabotaggi = {}
        numero_riunioni_organizzate = 0
        
        for m in meeting_mensili:
            lista = self.r_giorno.get_riunione_giorno(m)
            for l in lista.values():
                totals[l["colpevole"]] = totals.get(l["colpevole"], 0) + 1
                numero_vittime = len(l["vittime"])
                danno_riunione = l["durata"]*numero_vittime
                totale_sabotaggi[l["colpevole"]] = totale_sabotaggi.get(l["colpevole"], 0) + danno_riunione
            numero_riunioni_organizzate += 1

            
        if not totals: 
            return None
        sabateur = max(totals, key=totals.get)
        
        indice_sabotaggio = totale_sabotaggi[sabateur]
        response = {
            "manager" : sabateur,
            "riunioni_organizzate" : numero_riunioni_organizzate,
            "indice_sabotaggio" : indice_sabotaggio
        }
        return response

        
        #sabateur = max(totals, key=lambda x:totals[x]) # itera da solo


if __name__ == "__main__":
    p = Prenotazione()
    p.create_prenotazione("2025-12-19", "gerti", ["foo", "bar"], 1, "08:00") 
    p.create_prenotazione("2025-12-19", "foo", ["foo", "bar"], 1, "19:00")
    p.create_prenotazione("2025-12-20", "gerti", ["foo", "bar"], 1, "19:00") 
    r=RiunioneGiorno()
    print(r.get_riunione_giorno("2025-12-19"))

    riepilogo = RiepilogoGiorno()
    riepilogo.get_dettagli_giornata("2025-12-19")

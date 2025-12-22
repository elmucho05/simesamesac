from google.cloud import firestore


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

class RipilogoSettimana():
    def __init__(self):
        self.db = firestore.Client()
    
    def get_dettagli_settimana(self):
        pass

if __name__ == "__main__":
    p = Prenotazione()
    p.create_prenotazione("2025-12-19", "gerti", ["foo", "bar"], 1, "08:00")
    p.create_prenotazione("2025-12-19", "foo", ["foo", "bar"], 1, "19:00")
    p.create_prenotazione("2025-12-20", "gerti", ["foo", "bar"], 1, "19:00")
    r=RiunioneGiorno()
    print(r.get_riunione_giorno("2025-12-19"))

    riepilogo = RiepilogoGiorno()
    riepilogo.get_dettagli_giornata("2025-12-19")

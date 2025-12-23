#!/usr/bin/python3
from google.cloud import firestore
import datetime

db = firestore.Client()

def get_current_month_str():
    now = datetime.datetime.now()
    return now.strftime('%m-%Y')

def get_meetings_for_month(month_str):
    docs = db.collection('meeting_crimes').stream()
    
    meetings = []
    for doc in docs:
        if doc.id.endswith(month_str):
            meetings.append(doc.to_dict())
    return meetings

def calculate_totals(meetings):
    stats = {} 
    
    for day_data in meetings:
        for meeting in day_data.values():
            if not isinstance(meeting, dict):
                continue
            durata = float(meeting.get('durata', 0))
            organizzatore = meeting.get('colpevole')
            vittime = meeting.get('vittime', [])

            if organizzatore: 
                if organizzatore not in stats:
                    stats[organizzatore] = {'ore_totali': 0, 'riunioni_organizzate': 0}
                
                stats[organizzatore]['ore_totali'] += durata
                stats[organizzatore]['riunioni_organizzate'] += 1

            for v in vittime:
                if v not in stats:
                    stats[v] = {'ore_totali': 0, 'riunioni_organizzate': 0}
                stats[v]['ore_totali'] += durata

    return stats

def save_stats_to_db(month_str, stats_data):
    # creo una nuova collection
    db.collection('statistiche_mensili').document(month_str).set(stats_data)

def update_monthly_stats(request):
    mese_corrente = get_current_month_str()
    meetings = get_meetings_for_month(mese_corrente)
    stats = calculate_totals(meetings)
    save_stats_to_db(mese_corrente, stats)
    
    return 'Statistiche aggiornate per il mese %s. Utenti processati: %d' % (mese_corrente, len(stats))

if __name__ == '__main__':
    print(update_monthly_stats(None))
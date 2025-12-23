from datetime import datetime, time,timedelta
import calendar
def format_date_for_db(ui_date_str):
    """Converts 25-12-2023 -> 2023-12-25"""
    try:
        date_obj = datetime.strptime(ui_date_str, "%d-%m-%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None

def format_date_for_ui(db_date_str):
    """Converts 2023-12-25 -> 25-12-2023"""
    try:
        date_obj = datetime.strptime(db_date_str, "%Y-%m-%d")
        return date_obj.strftime("%d-%m-%Y")
    except ValueError:
        return db_date_str
def date_from_str(d):
    """
    Converts a string to a datetime object.
    Supports both 'YYYY-MM-DD' (Swagger/API standard) and 'DD-MM-YYYY' (Prof standard).
    """
    if not d:
        return None
        
    # Try ISO format first (YYYY-MM-DD) - This is what Swagger sends
    # try:
    #     return datetime.strptime(d, '%Y-%m-%d')
    # except ValueError:
    #     pass

    # Try Italian format (DD-MM-YYYY)
    try:
        return datetime.strptime(d, '%d-%m-%Y')
    except ValueError:
        return None 
    
def str_from_date(d):
    """Converts datetime object to 'YYYY-MM-DD' string"""
    if d is None:
        return ""
    return d.strftime('%Y-%m-%d')

def time_from_str(t):
    """Converts 'HH:MM' string to time object"""
    try:
        # FIXED: removed 'datetime.datetime'
        return datetime.strptime(t, '%H:%M').time()
    except (ValueError, TypeError):
        return None
def calculate_end_time(start_time_string, duration):
    """Calcola l'orario di fine dato l'orario d'inizio e la durata"""
    try:
        # Assuming time_from_str is defined elsewhere in your code
        start_time = time_from_str(start_time_string) 
        
        # --- THE FIX IS HERE ---
        # Changed 'start_minute' to 'start_time.minute'
        start_minutes = start_time.hour * 60 + start_time.minute
        
        # Calculate total end minutes
        end_minutes = start_minutes + int(duration * 60)

        # Convert back to hours and minutes
        # We use % 24 to handle cases where the time goes past midnight (e.g., 25:00 -> 01:00)
        end_hour = (end_minutes // 60) % 24
        end_minute = end_minutes % 60

        return time(end_hour, end_minute)
    except ValueError:
        return None
    
def parse_month(month_str):
    """converte 'MM-YYYY' in oggetto datetime"""
    try:
        return datetime.strptime(month_str, '%m-%Y').date()
    except ValueError:
        return None

def get_week_dates():
    datetime.today().weekday()

    today = datetime.today()

    start_of_week = today - timedelta(days=today.weekday())

    week_dates = []
    for i in range(5): #5 giorni lavorativi
        current_day = start_of_week + timedelta(days=i)
        week_dates.append(current_day.strftime("%d-%m-%Y")) 

    return week_dates 

# def get_month_dates():
#     today = datetime.today().date().replace(day=1) # to get the same as the prof
#     start_of_month = today.min.day
#     end_of_month = today.max.day
#     month_days = []
#     stringa = ""
#     for i in range(start_of_month, end_of_month+1): #5 giorni lavorativi
#         stringa = f"{i}-{today.month}-{today.year}" 
#         month_days.append(stringa)

#     return month_days

def get_month_dates():
    today = datetime.today().date()
    
    _, last_day = calendar.monthrange(today.year, today.month)
    
    month_days = []
    for i in range(1, last_day + 1):
        current_date = today.replace(day=i) # to get the same as the prof format
        month_days.append(current_date.strftime("%d-%m-%Y"))
    return month_days

def estrai_mese_ordinabile(date_str):
    """ Converte '23-12-2025' in '2025-12' """
    try:
        parts = date_str.split("-") # ["23", "12", "2025"]
        return f"{parts[2]}-{parts[1]}"
    except:
        return None 
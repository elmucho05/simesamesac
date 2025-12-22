from datetime import datetime, time
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
    try:
        return datetime.strptime(d, '%Y-%m-%d')
    except ValueError:
        pass

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
import datetime

def _get_timestamp():
    return datetime.datetime.now().strftime('%H:%M:%S')

def log_info(message: str):
    print(f"[{_get_timestamp()}] {message}")

def log_error(message: str):
    print(f"[{_get_timestamp()}] ERROR: {message}")

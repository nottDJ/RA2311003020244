import requests
import os
import importlib.util

# --- LOGGER IMPORT WORKAROUND ---
logger_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logging middleware', 'logger.py'))
spec = importlib.util.spec_from_file_location("logger_module", logger_path)
logger_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logger_module)
# --------------------------------

# Using your brand new token
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJkcDEyNDVAc3JtaXN0LmVkdS5pbiIsImV4cCI6MTc3NzcwMzU1NSwiaWF0IjoxNzc3NzAyNjU1LCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiYjQ2MGM0YzUtYTkxNC00Zjg5LWFlMDItMTk3ZWE4ZTc1ZDc4IiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoiZGl2aWogayBwIiwic3ViIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIn0sImVtYWlsIjoiZHAxMjQ1QHNybWlzdC5lZHUuaW4iLCJuYW1lIjoiZGl2aWogayBwIiwicm9sbE5vIjoicmEyMzExMDAzMDIwMjQ0IiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIiwiY2xpZW50U2VjcmV0IjoiRHZnWGdDSHl5Rk10U0Z6cCJ9.3ii813bVAshw7fSnOKNvJQkJezgOmFE56NXowNw-BFY"

API_URL = "http://20.207.122.201/evaluation-service/notifications"

def get_notifications():
    headers = {"Authorization": "Bearer " + TOKEN}
    try:
        response = requests.get(API_URL, headers=headers)
        if response.status_code == 200:
            logger_module.send_log("backend", "info", "api", "Successfully fetched notifications")
            return response.json()["notifications"]
        else:
            logger_module.send_log("backend", "error", "api", "Failed to get notifications")
            return []
    except Exception as e:
        logger_module.send_log("backend", "fatal", "api", "Network error")
        return []

def sort_priority_inbox(notifications):
    logger_module.send_log("backend", "info", "handler", "Sorting notifications by priority")
    
    for notif in notifications:
        if notif["Type"] == "Placement":
            notif["score"] = 3
        elif notif["Type"] == "Result":
            notif["score"] = 2
        elif notif["Type"] == "Event":
            notif["score"] = 1
        else:
            notif["score"] = 0

    def sorting_logic(n):
        return (n["score"], n["Timestamp"])

    notifications.sort(key=sorting_logic, reverse=True)

    top_10 = []
    count = 0
    for n in notifications:
        if count < 10:
            top_10.append(n)
            count += 1
        else:
            break
            
    return top_10

if __name__ == "__main__":
    print("Fetching notifications...\n")
    
    all_notifs = get_notifications()
    
    if all_notifs:
        top_notifications = sort_priority_inbox(all_notifs)
        
        print("--- Top 10 Priority Notifications ---")
        for i in range(len(top_notifications)):
            item = top_notifications[i]
            print(str(i + 1) + ". [" + item["Type"] + "] " + item["Message"] + " - " + item["Timestamp"])
    else:
        print("Error: Could not fetch data. Check your token.")

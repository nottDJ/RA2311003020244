import requests

def send_log(stack, level, package_name, message):
    """
    A simple function to send logs to the evaluation server.
    """
    url = "http://20.207.122.201/evaluation-service/logs"
    
    # Put your saved access token right here inside the quotes
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJkcDEyNDVAc3JtaXN0LmVkdS5pbiIsImV4cCI6MTc3NzcwMzU1NSwiaWF0IjoxNzc3NzAyNjU1LCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiYjQ2MGM0YzUtYTkxNC00Zjg5LWFlMDItMTk3ZWE4ZTc1ZDc4IiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoiZGl2aWogayBwIiwic3ViIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIn0sImVtYWlsIjoiZHAxMjQ1QHNybWlzdC5lZHUuaW4iLCJuYW1lIjoiZGl2aWogayBwIiwicm9sbE5vIjoicmEyMzExMDAzMDIwMjQ0IiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIiwiY2xpZW50U2VjcmV0IjoiRHZnWGdDSHl5Rk10U0Z6cCJ9.3ii813bVAshw7fSnOKNvJQkJezgOmFE56NXowNw-BFY" 

    # Set up the headers with your token
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }

    # Prepare the data exactly how the server expects it
    data = {
        "stack": stack,
        "level": level,
        "package": package_name,
        "message": message
    }

    # Send the request
    try:
        requests.post(url, headers=headers, json=data)
    except:
        # If the network fails, we just ignore it so it doesn't crash our main app
        pass
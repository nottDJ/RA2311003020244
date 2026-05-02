import requests

def send_log(stack, level, package_name, message):
    """
    A simple function to send logs to the evaluation server.
    """
    url = "http://20.207.122.201/evaluation-service/logs"
    
    # Put your saved access token right here inside the quotes
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJkcDEyNDVAc3JtaXN0LmVkdS5pbiIsImV4cCI6MTc3NzcwMjE1NiwiaWF0IjoxNzc3NzAxMjU2LCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiOWIxY2FkNDEtYTIwZi00ZWUxLTk4OTctMjU2NjA5YmE3YmFkIiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoiZGl2aWogayBwIiwic3ViIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIn0sImVtYWlsIjoiZHAxMjQ1QHNybWlzdC5lZHUuaW4iLCJuYW1lIjoiZGl2aWogayBwIiwicm9sbE5vIjoicmEyMzExMDAzMDIwMjQ0IiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIiwiY2xpZW50U2VjcmV0IjoiRHZnWGdDSHl5Rk10U0Z6cCJ9.ekWCjsMYfZwGW_Gp84RdSwTHyt_JADoZj8FnvEJxP7c" 

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
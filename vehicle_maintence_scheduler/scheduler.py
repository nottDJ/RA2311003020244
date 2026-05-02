import requests
import sys
import os
import importlib.util

# --- LOGGER IMPORT WORKAROUND ---
# Because "logging middleware" has a space, standard Python 'import' fails. 
# This safely loads your logger file dynamically.
logger_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logging middleware', 'logger.py'))
spec = importlib.util.spec_from_file_location("logger_module", logger_path)
logger_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(logger_module)
# --------------------------------

# Paste your saved token right here
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJkcDEyNDVAc3JtaXN0LmVkdS5pbiIsImV4cCI6MTc3NzcwMzU1NSwiaWF0IjoxNzc3NzAyNjU1LCJpc3MiOiJBZmZvcmQgTWVkaWNhbCBUZWNobm9sb2dpZXMgUHJpdmF0ZSBMaW1pdGVkIiwianRpIjoiYjQ2MGM0YzUtYTkxNC00Zjg5LWFlMDItMTk3ZWE4ZTc1ZDc4IiwibG9jYWxlIjoiZW4tSU4iLCJuYW1lIjoiZGl2aWogayBwIiwic3ViIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIn0sImVtYWlsIjoiZHAxMjQ1QHNybWlzdC5lZHUuaW4iLCJuYW1lIjoiZGl2aWogayBwIiwicm9sbE5vIjoicmEyMzExMDAzMDIwMjQ0IiwiYWNjZXNzQ29kZSI6IlFrYnB4SCIsImNsaWVudElEIjoiMzYyNGY0ZjUtMzFiNy00OWYwLWIzOGQtMDgwMTRjZWQ3ZWEwIiwiY2xpZW50U2VjcmV0IjoiRHZnWGdDSHl5Rk10U0Z6cCJ9.3ii813bVAshw7fSnOKNvJQkJezgOmFE56NXowNw-BFY"

def get_data(endpoint):
    """Fetches data from the Affordmed API"""
    url = "http://20.207.122.201/evaluation-service/" + endpoint
    headers = {"Authorization": "Bearer " + TOKEN}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            logger_module.send_log("backend", "info", "api", "Successfully fetched " + endpoint)
            return response.json()
        else:
            logger_module.send_log("backend", "error", "api", "Failed to fetch " + endpoint)
            return None
    except Exception as e:
        logger_module.send_log("backend", "fatal", "api", "Network error: " + str(e))
        return None

def optimize_maintenance(mechanic_hours, vehicles):
    """
    Finds the best combination of vehicles to service.
    This uses a basic Dynamic Programming table (0/1 Knapsack).
    """
    num_vehicles = len(vehicles)
    
    # Create a 2D grid to track the max impact for different hour limits
    dp = []
    for i in range(num_vehicles + 1):
        row = [0] * (mechanic_hours + 1)
        dp.append(row)
        
    # Fill out the grid
    for i in range(1, num_vehicles + 1):
        current_vehicle = vehicles[i - 1]
        duration = current_vehicle["Duration"]
        impact = current_vehicle["Impact"]
        
        for current_hours in range(mechanic_hours + 1):
            if duration <= current_hours:
                # We have enough hours to include this vehicle. Let's see if it's worth it.
                include_impact = impact + dp[i - 1][current_hours - duration]
                exclude_impact = dp[i - 1][current_hours]
                dp[i][current_hours] = max(include_impact, exclude_impact)
            else:
                # Not enough hours, we must skip this vehicle
                dp[i][current_hours] = dp[i - 1][current_hours]
                
    # Now, work backwards through the grid to figure out WHICH vehicles we actually chose
    max_impact = dp[num_vehicles][mechanic_hours]
    chosen_tasks = []
    
    hours_left = mechanic_hours
    for i in range(num_vehicles, 0, -1):
        if dp[i][hours_left] != dp[i - 1][hours_left]:
            selected_vehicle = vehicles[i - 1]
            chosen_tasks.append(selected_vehicle["TaskID"])
            hours_left -= selected_vehicle["Duration"]
            
    return max_impact, chosen_tasks

if __name__ == "__main__":
    logger_module.send_log("backend", "info", "service", "Starting Vehicle Maintenance script")
    print("Fetching depots and vehicles data from server...\n")
    
    depots_data = get_data("depots")
    vehicles_data = get_data("vehicles")
    
    if depots_data and vehicles_data:
        depots = depots_data["depots"]
        vehicles = vehicles_data["vehicles"]
        
        # Calculate the best schedule for every single depot
        for depot in depots:
            depot_id = depot["ID"]
            hours_budget = depot["MechanicHours"]
            
            print("--------------------------------------------------")
            print("Processing Depot ID: " + str(depot_id) + " (Budget: " + str(hours_budget) + " hours)")
            
            best_impact, selected_tasks = optimize_maintenance(hours_budget, vehicles)
            
            print("Maximum Impact Achieved: " + str(best_impact))
            print("Number of Vehicles Serviced: " + str(len(selected_tasks)))
            print("Selected Task IDs:")
            for task in selected_tasks:
                print(" - " + task)
            print("")
            
            logger_module.send_log("backend", "info", "service", "Finished optimizing Depot " + str(depot_id))
            
    else:
        print("Error: Could not retrieve data. Please check your token.")
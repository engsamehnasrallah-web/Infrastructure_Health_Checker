import json 

def load_config():
    try:
        with open("config/config.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Error: config/config.json not found.")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in config/config.json.")
        return {}
import json
data_model = {
    "users":{
        "admin":{
            "password": "admin1234" ,
            "tasks":[]
        }
}
}
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError , json.JSONDecodeError):
        return data_model
def save_data():
    try: 
        with open("data.json", "w") as file:
            return json.dump(file)
    except:
        print("wasn't possible saving your data, try again")
def main():
    pass

if __name__ == "__main__":
    main()
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
def save_data(data):
  with open("data.json", "w") as file:
    json.dump(data , file)

def register(data, user_name, password):
    users = data['users']
    _user_name = user_name.lower()
    _password = password.strip()
    if not user_name or not _password :
        print("Invalid input ")
        return
    if _user_name in users:
       print("User already exists")
       print(f"{_user_name} {users[_user_name]}")
       return
    else:
   
        users[_user_name] = {"password": _password , "tasks" : []}
        print(f" user created:\n {_user_name} {users[_user_name]}")
        save_data(data)

def main():
    data = load_data()
    register(data , "" , "")

if __name__ == "__main__":
    main()
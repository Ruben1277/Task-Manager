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
    try: 
        with open("data.json", "w") as file:
            return json.dump(data , file)
    except:
        print("wasn't possible saving your data, try again")
def register(data, user_name, password):
    users = data['users']
    _user_name = user_name.lower()
    _password = password.lower()
    if _user_name in users.keys():
        if users[_user_name]["password"] == password:
            print(users[_user_name])
        else:
            print("password invalid try again")
    else:
        print("new login")
        users[_user_name] = {"password": _password , "tasks" : []}
        data['users'] = users
        print(f"{_user_name} {users[_user_name]}")
        save_data(data)

def main():
    data = load_data()
    register(data , "gamer" , "jon11")

if __name__ == "__main__":
    main()
import json
#note: add tomorrow : add login feature with validation and password hashing for security
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
def login(data , user_name, password):
    users = data['users']
    _user_name = user_name.lower().strip()
    #use hash next to inprove the security
    _password = password.strip()
    if not _user_name or not _password :
        print("Invalid input ")
        return False
    if _user_name in users:
        if _password == users[_user_name]['password']:
            print(f"Login sucessful")
            return True
        else:
            print('Incorrect password, try again')
            return False
    else:
        print("User don't exist, try other user")
        return False

    
def register(data, user_name, password):
    users = data['users']
    _user_name = user_name.lower().strip()
    #use hash next to inprove the security
    _password = password.strip()
    if not _user_name or not _password :
        print("Invalid input ")
        return False
    if _user_name in users:
       print("User already exists")
       print(f"{_user_name} {users[_user_name]}")
       return False
    else:
   
        users[_user_name] = {"password": _password , "tasks" : []}
        print(f" user created:\n {_user_name} {users[_user_name]}")
        save_data(data)
        return True

def main():
    data = load_data()
    login(data , "rub" , "111")
    
if __name__ == "__main__":
    main()

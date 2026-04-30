import json
import os
import hashlib 
#note: add tomorrow : add login feature with validation and password hashing for security
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
data_model = {
    "users":{
        "admin":{
            "password": hash_password("admin1234") ,
            "tasks":[]
        }
}
}

# Load data and solve errors

def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except (FileNotFoundError , json.JSONDecodeError):
        return data_model
    
    #Save data and solve errors

def save_data(data):
  with open("data.json", "w") as file:
    json.dump(data , file)
    #login with validation
def login(data , user_name, password):
    users = data['users']
    _user_name = user_name.lower().strip()
    #validation on position wrong, solve tomorrow
    _password = hash_password(password.strip())
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

    #register with validation
def register(data, user_name, password):
    
    users = data['users']
    _user_name = user_name.lower().strip()
    #validation on position wrong, solve tomorrow
    _password = hash_password(password.strip())
    if not _user_name or not _password :
        print("Invalid input ")
        return False
    if _user_name in users:
       print("User already exists")
       return False
    else:
   
        users[_user_name] = {"password": _password , "tasks" : []}
        save_data(data)
        return True
def cancel():
    pass
def input_control(input_type, data):
    match input_type :
        case 'login':
            username = input(menu('login_username'))
            password = input(menu('login_password'))
            login(data, username, password)
        case 'register':
            username = input(menu('register_username'))
            password = input(menu('register_password'))    
            register(data , username, password)        
        case _:
            print('Write a valid function: ')
def clear_terminal():
    #this is limited to windows, solce tomorrow for other OS
    os.system("cls")

def menu(menu_mode):
    match menu_mode:
        case 'main':
            #mixed with clear terminal, solve tomorrow
            clear_terminal()
            return('Feats: |1| login , |2| register , |3| delete account , |4| show account \n')
        case 'login_username':
                clear_terminal()
                return "Write your username: "
        case 'login_password':
                clear_terminal()
                return "Write your password: "  
        case 'register_username':
            clear_terminal()
            return "Make your username: "
        case 'register_password':
            clear_terminal()
            return "Make your password: "
                 


def main():
    print(menu("main"))
    data = load_data()
    #solve the flux of system and add a loop to control the system
    input_control('register', data)
    
if __name__ == "__main__":
    main()

import json
import os
import hashlib 

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

    if not _user_name or not password.strip() :
        print("Invalid input ")
        return False , None
    _password = hash_password(password.strip())

    if _user_name in users:
        if _password == users[_user_name]['password']:
            print(f"Login sucessful")
            return True , _user_name
        else:
            print('Incorrect password, try again')
            return False, None
        
    else:
        print("User don't exist, try other user")
        return False , None

    #register with validation
def register(data, user_name, password):
    
    users = data['users']
    _user_name = user_name.lower().strip()
    if not _user_name or not password.strip() :
        print("Invalid input ")
        return False , None

    _password = hash_password(password.strip())

    if _user_name in users:
       print("User already exists")
       return False , None
    else:
        users[_user_name] = {"password": _password , "tasks" : []}
        save_data(data)
        return True , _user_name
def cancel():
    pass
def input_control(input_type, data):
    match input_type :
        case '1':
            username = input(menu('login_username'))
            password = input(menu('login_password'))
            sucess, current_user = login(data, username, password)
            if sucess:
                return current_user
            else:
                print( 'Not possible login , try again later: ')
        case '2':
            username = input(menu('register_username'))
            password = input(menu('register_password'))    
            sucess , current_user = register(data , username, password)    
            if sucess:
                return current_user
            else:
                print('Not possible register , try again later')
                return False 
        case _:
            print('Write a valid function: ')
            return False
def clear_terminal():

    os.system("cls" if os.name == 'nt' else 'clear')

def menu(menu_mode):
    match menu_mode:
        case 'main':
            return('Feats: |1| login , |2| register , |3| delete account , |4| show account , |5| exit\n')
        case 'login_username':
                return "Write your username: "
        case 'login_password':
                return "Write your password: "  
        case 'register_username':
            return "Make your username: "
        case 'register_password':
            return "Make your password: "
                 


def main():
    clear_terminal()
    data = load_data()
    current_user = None
    while True:
        print(menu('main'))
        choice_function = input('Which fuction your want to execute: ')
        if choice_function == '5':
            break
        _current_user = input_control(choice_function, data)
        if _current_user:
            current_user = _current_user
        print(f"Current User : {current_user}")
        input('Press Enter to continue: ')
        clear_terminal()
    
if __name__ == "__main__":
    main()

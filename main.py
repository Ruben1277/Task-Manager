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
            print(f"Login successful")
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
def add_task(task, data , current_user):
    if current_user is None:
        print('You need to do login for make tasks: ')
        return None
    if current_user.strip().lower() in data['users']:
        tasks = data['users'][current_user.strip().lower()]['tasks']  
        tasks.append({'task':task , 'check':False})
        print('Task created with success')
        save_data(data)
        return True
    else:
        print('This user not exist: ')
        return None
def show_tasks(data, current_user):
    if current_user is None:
        print('You need to do login for show tasks: ')
        return None
    else:
        if current_user.strip().lower() in data['users']:
            tasks = data['users'][current_user.strip().lower()]['tasks']
            if not tasks:
                print('No tasks found')
                return None
            else:
                print(f"Tasks for {current_user}:")
                for index, task in enumerate(tasks):
                    print(f"|{index}| : {task}")
                return True
def check_task(data, current_user, task_index):
    try: 
        _current_user = current_user.strip().lower()
    except AttributeError:
        _current_user = current_user
    if _current_user is None:
        print("You need to login for check your tasks: ")
        return None
    else:
        if _current_user in data['users']:
            tasks = data['users'][_current_user]['tasks']
            if 0 <= task_index < len(tasks):
                tasks[0]['check'] = True
                save_data(data)
                return True
            else:
                print("no have tasks, create a task first: ")
                return None
        else:
            print('User not was finded')
            return None

def delete_task():
    pass
def cancel():
    pass
def input_control(input_type, data, current_user):
    match input_type.strip().lower() :
        case '1':
            username = input(menu('login_username'))
            password = input(menu('login_password'))
            success, _current_user = login(data, username, password)
            if success:
                return _current_user
            else:
                print( 'Not possible login , try again later: ')
                return None
        case '2':
            username = input(menu('register_username'))
            password = input(menu('register_password'))    
            success , _current_user = register(data , username, password)    
            if success:
                return _current_user
            else:
                print('Not possible register , try again later')
                return None
        case '3':
            task = input(menu('task'))
            success = add_task(task, data, current_user)
            if success :
                return current_user
            else:
                return None
        case '4':
            success = show_tasks(data, current_user)
            if success:
                return current_user
            else:
                return None
        case '5':
            success = check_task(data, current_user, 0)
            if success:
                return current_user
            else:
                return None           
        case _:
            print('Write a valid function: ')
            return None
def clear_terminal():

    os.system("cls" if os.name == 'nt' else 'clear')

def menu(menu_mode):
    match menu_mode:
        case 'main':
            return('Feats: |1| login , |2| register , |3| add task , |4| show tasks , |5| check task , |6| exit\n')
        case 'login_username':
                return "Write your username: "
        case 'login_password':
                return "Write your password: "  
        case 'register_username':
            return "Make your username: "
        case 'register_password':
            return "Make your password: "
        case 'task':
            return "What task your want to add on the task list, write a task: "


def main():
    clear_terminal()
    data = load_data()
    current_user = None
    while True:
        print(menu('main'))
        choice_function = input('Which fuction your want to execute: ').strip().lower()
        if choice_function == '6':
            break
        _current_user = input_control(choice_function, data, current_user)
        if _current_user is not None:
            current_user = _current_user
        print(f"Current User : {current_user}")
        input('Press Enter to continue: ')
        clear_terminal()
    save_data(data)
    
if __name__ == "__main__":
    main()

import json
import os
import hashlib 

# MELHORIA: adicione constantes para mensagens repetidas
# MELHORIA: use pathlib.Path para caminhos de arquivo
# MELHORIA: adicione logging para debug 

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
        return data_model  # MELHORIA: log o erro para debug
    
    #Save data and solve errors

def save_data(data):
  with open("data.json", "w") as file:
    json.dump(data , file , indent = 4)  # ERRO: JSON sem indentação fica ilegível. Sugestão: adicione indent=4
    #login with validation
def adjust_str_input(str_input):
    try:
        return str_input.strip().lower()
    except AttributeError :
        return None
def login(data , user_name, password):
    users = data['users']
    _user_name = user_name.lower().strip()

    if not _user_name or not password.strip() :  # ERRO: inconsistente - password.strip() aqui, mas password em outros lugares
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
    if not _user_name or not password.strip() :  # MELHORIA: use password.strip() consistentemente
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
    _current_user = adjust_str_input(current_user)
    if _current_user is None:
        print('You need to do login for make tasks: ')
        return None
    if _current_user in data['users']:
        tasks = data['users'][_current_user]['tasks']  
        tasks.append({'task':task , 'check':False})
        print('Task created with success')
        save_data(data)
        return True
    else:
        print('This user not exist: ')
        return None
def show_tasks(data, current_user):
    _current_user = adjust_str_input(current_user)
    if _current_user is None:
        print('You need to do login for show tasks: ')
        return None
    else:
        if _current_user in data['users']:
            tasks = data['users'][_current_user]['tasks']
            if not tasks:
                print('No tasks found')
                return None
            else:
                print(f"Tasks for {_current_user}:")
                for index, task in enumerate(tasks):
                    print(f"|{index}| : {task['task']} [{'✅' if task['check'] == True else '❌'}]")
                    print("-"*50)  # ERRO: imprime dicionário inteiro, deve ser task['task']
                return True
def check_task(data, current_user, task_index):
    _current_user = adjust_str_input(current_user)
    if _current_user is None:
        print("You need to login for check your tasks: ")
        return None
    else:
        if _current_user in data['users']:
            tasks = data['users'][_current_user]['tasks']
            if 0 <= task_index < len(tasks):  # MELHORIA: adicione mensagem específica para índice inválido
                tasks[task_index]['check'] = True
                save_data(data)
                return True
            else:
                print("no have tasks, create a task first: ")
                return None
        else:
            print('User not was finded')
            return None

def delete_task(data, current_user , task_index):
    _current_user = adjust_str_input(current_user)
    if _current_user is None:
        print("You need to login for check your tasks: ")
        return None
    else:
        if _current_user in data['users']:
            tasks = data['users'][_current_user]['tasks']
            if 0 <= task_index < len(tasks):  # MELHORIA: adicione mensagem específica para índice inválido
                task_removed = tasks.pop(task_index)
                save_data(data)
                return True
            else:
                print("no have tasks, create a task first: ")
                return None
        else:
            print('User not was finded')
            return None

def get_input(prompt):
    while True:
        value = input(f"{prompt} or write |cancel| to cancel: ").strip()
        if value.lower() == 'cancel':
            is_sure = input('are you sure, you are canceling |y| or |n| for confirm: ').strip().lower()
            if is_sure == 'y':
                return None
            else :
                continue
        return value
def input_control(input_type, data, current_user):
    match input_type.strip().lower() :  # MELHORIA: adicione validação se input_type é válido antes do match
        case '1':
            username = get_input(menu('login_username'))
            if username is None:
                return None
            password = get_input(menu('login_password'))
            if password is None:
                return None
            success, _current_user = login(data, username, password)
            if success:
                return _current_user
            else:
                print( 'Not possible login , try again later: ')

                return None
        case '2':
            username = get_input(menu('register_username'))
            if username is None:
                return None
            password = get_input(menu('register_password'))    
            if password is None:
                return None
            success , _current_user = register(data , username, password)    
            if success:
                return _current_user
            else:
                print('Not possible register , try again later')
                return None
        case '3':
            task = get_input(menu('task'))
            if task is None:
                return None
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
            task_index = get_input('Write the index of task for check it: ')
            if task_index is None:
                return None
            try:
                task_index = int(task_index)
            except ValueError:
                print('Write a valid index: ')
                return None
            success = check_task(data, current_user, task_index)
            if success:
                return current_user
            else:
                return None    
        case '6':
            task_index = get_input('Write the index of task for delete it: ')
            if task_index is None:
                return None
            try:
                task_index = int(task_index)
            except ValueError:
                print('Write a valid index: ')
                return None    
            success = delete_task(data , current_user, task_index)
            if success :
                return current_user
            else:
                return None
        case _:
            print('Write a valid function: ')
            return None
def clear_terminal():

    os.system("cls" if os.name == 'nt' else 'clear')  # MELHORIA: use subprocess.run() para melhor segurança

def menu(menu_mode):
    match menu_mode:  # MELHORIA: use dicionário para menus ou classe para melhor organização
        case 'main':
            return('Feats: |1| login , |2| register , |3| add task , |4| show tasks , |5| check task , |6| delete task , |7| exit\n')
        case 'login_username':
                return "Write your username"
        case 'login_password':
                return "Write your password"  
        case 'register_username':
            return "Make your username"
        case 'register_password':
            return "Make your password"
        case 'task':
            return "What task your want to add on the task list, write a task"

def main():
    clear_terminal()
    data = load_data()
    current_user = None
    
    while True:
        print(menu('main'))
        choice_function = input('Which fuction your want to execute: ').strip().lower()  # ERRO: "fuction" deve ser "function"
        if choice_function == '7':
            break
        _current_user = input_control(choice_function, data, current_user)
        if _current_user is not None:
            current_user = _current_user
        print(f"Current User : {current_user}")  # MELHORIA: só imprima se current_user não for None
        input('Press Enter to continue: ')
        clear_terminal()
    save_data(data)
    
if __name__ == "__main__":
    main()
# MELHORIA GERAL: considere usar classes para organizar o código (ex: UserManager, TaskManager)
# MELHORIA: adicione testes unitários
# MELHORIA: use type hints para melhor legibilidade

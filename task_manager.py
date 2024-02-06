# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date
from pprint import pprint


# function to register new user and add their username and password to the user.txt file
def register_new_user():
    """
    Add a new user to the user.txt file
    Check if username already exists. If so,
    display relevant error message
    and allow them to try to add a user with a different username
    """

    while True:
        # - Request input of a new username
        new_username = input("New Username: ").lower()

        # open the user.txt file
        with open('user.txt', 'r') as u_file:
            # check if username already exists. If so, user is asked to enter different username
            if new_username in u_file.read():
                print("This username already exists. Enter a different username")
            elif new_username not in u_file.read():
                break

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password

        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    '''Allow a user to add a new task to task.txt file
         Prompt a user for the following:
          - A username of the person whom the task is assigned to,
          - A title of a task,
          - A description of the task and
          - the due date of the task.
          '''

    # ask user to input name of person assigned to task. If user doesn't exist, give option to input again.
    while True:
        task_username = input("Name of person assigned to task: ").lower()
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''

    task_num = str(len(task_list) + 1)
    new_task = {
        "task number": task_num,
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            # add task num
            str_attrs = [
                t['task number'],
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def get_tasks(all_tasks, user_name=None):
    if user_name is None:
        return all_tasks
    else:
        tasks = []
        for task in all_tasks:
            if task['username'] == user_name:
                tasks.append(task)
        return tasks


def display_tasks(tasks):
    '''Reads the task from task.txt file and prints to the console in the
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling)
    '''

    for t in tasks:
        # add task num
        disp_str = f"Task Number: \t {t['task number']}\n"
        disp_str += f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n\t {t['description']}\n"
        print(disp_str)

    choice_of_task = input("If you would like to select task, enter task number or press -1 to return to Main menu. ")

    if choice_of_task == "-1":
        return

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""] # list of strings ['1;admin;Add functionality to task manager' '2;username;task' etc.]


task_dict = {}
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")

    # task num
    curr_t['task number'] = task_components[0]
    curr_t['username'] = task_components[1]
    curr_t['title'] = task_components[2]
    curr_t['description'] = task_components[3]
    curr_t['due_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[5], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[6] == "Yes" else False

    task_dict[curr_t['task number']] = curr_t  # dictionary of dictionaries with "key"= task number & "value" = whole task
    task_list.append(curr_t)  # list of dictionaries
# print(task_dict)
# print(task_list)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        register_new_user()

    elif menu == 'a':
        add_task()

    elif menu == 'va':
        display_tasks(get_tasks(task_list, None))

    elif menu == 'vm':
        display_tasks(get_tasks(task_list, user_name=curr_user))


    elif menu == 'ds' and curr_user == 'admin':
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")

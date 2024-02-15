# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import datetime, date


def add_number_1_to_first_task():
    # read tasks from file
    with open("tasks.txt", "r") as f:
        # split the file contents into a list based on the location of the semicolon
        first_task = f.read().split(";")

    # check if the first task number is 1 and if not, add 1 to the first task number
    if first_task[0][0] != "1":
        first_task.insert(0, "1")
        first_task_string = ";".join(first_task)
        # write updated task back to the tasks file
        with open("tasks.txt", "w") as f:
            f.write(first_task_string)


# function to register new user and add their username and password to the user.txt file
def register_new_user(username_password_dict):
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
        username_password_dict[new_username] = new_password

        # write new user and their password into the user.txt file
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password_dict:
                user_data.append(f"{k};{username_password_dict[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task(username_password_dict, date_format, all_tasks_list):
    """Allow a user to add a new task to task.txt file
         Prompt a user for the following:
          - A username of the person whom the task is assigned to,
          - A title of a task,
          - A description of the task and
          - the due date of the task."""

    # ask user to input name of person assigned to task. If user doesn't exist, give option to input again.
    while True:
        task_username = input("Name of person assigned to task: ").lower()
        if task_username not in username_password_dict.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, date_format)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''

    task_num = str(len(all_tasks_list) + 1)
    new_task = {
        "task number": task_num,
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    all_tasks_list.append(new_task)
    write_tasks_to_file(all_tasks_list, date_format)
    print("Task successfully added.")


def write_tasks_to_file(tasks, date_format):
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in tasks:
            # add task number to the string that represents task
            str_attrs = [
                t['task number'],
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(date_format),
                t['assigned_date'].strftime(date_format),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))


def get_tasks(all_tasks, user_name=None):
    # function returns all tasks or if user_name is specified, it will display tasks assigned to that user
    if user_name is None:
        return all_tasks
    else:
        tasks = []
        for task in all_tasks:
            if task['username'] == user_name:
                tasks.append(task)
        return tasks


def convert_user_assigned_tasks_to_dict(user_assigned_tasks_list):
    # function converts tasks assigned to a user into dictionary
    user_assigned_tasks_dict = {}
    for item in user_assigned_tasks_list:
        task_number = item['task number']
        user_assigned_tasks_dict[task_number] = item
    return user_assigned_tasks_dict


def mark_task_as_complete(all_tasks, task_chosen_by_user, date_format):
    # find the chosen task number in all task list and if task not completed, change to Yes (completed)
    for task in all_tasks:
        # check if task is marked as incomplete and if so, change the "completed" status to Yes (True)
        if task["task number"] == task_chosen_by_user and task["completed"] is False:
            task["completed"] = True
            print(f"The task no {task_chosen_by_user} has been marked as completed.")
            # print(all_tasks)

        elif task["task number"] == task_chosen_by_user and task["completed"] is True:
            # if the task is marked as completed, display the relevant message.
            print("The task has already been marked as completed.")

    # mark the relevant task in the tasks.txt file
    write_tasks_to_file(all_tasks, date_format)

    print(all_tasks)


def display_tasks(tasks, date_format):
    """Reads the task from task.txt file and prints to the console in the
       format of Output 2 presented in the task pdf (i.e. includes spacing
       and labelling)"""

    for t in tasks:
        # add task num
        disp_str = f"Task Number: \t {t['task number']}\n"
        disp_str += f"Task: \t\t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(date_format)}\n"
        disp_str += f"Due Date: \t\t {t['due_date'].strftime(date_format)}\n"
        disp_str += f"Task Description: \n\t {t['description']}\n"
        print(disp_str)


def edit_task_owner(task, username_passw_dict):
    # Function to change owner of a task
    while True:
        task_username = input("Who do you want to assign this task to: ").lower()
        if task_username not in username_passw_dict.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break
    task['username'] = task_username
    return task


def edit_due_date(task, date_format):
    # function to change due date of a selected task
    new_due_date = input("What date would you like to change this to? ")
    task['due_date'] = datetime.strptime(new_due_date, date_format)
    return task


def generate_task_overview(all_tasks):
    # function creates task overview text file displaying relevant statistics
    number_of_all_tasks = len(all_tasks)
    total_incomplete = 0
    total_overdue_incomplete_tasks = 0
    for task in all_tasks:
        if task["completed"] is False:
            total_incomplete += 1
            due_date = task["due_date"]
            todays_date = datetime.today()
            if due_date < todays_date:
                total_overdue_incomplete_tasks += 1
    total_completed_tasks = number_of_all_tasks - total_incomplete
    percentage_of_incomplete_tasks = (total_incomplete / number_of_all_tasks) * 100
    percentage_of_overdue_tasks = (total_overdue_incomplete_tasks * 100) / number_of_all_tasks

    task_overview_string = f"Task Overview\nNumber of all tasks = {number_of_all_tasks}\n" \
                           f"Total number of completed tasks = {total_completed_tasks}\n" \
                           f"Total number of uncompleted tasks = {total_incomplete}\n" \
                           f"Total number of overdue & uncompleted tasks = {total_overdue_incomplete_tasks}\n" \
                           f"Percentage of uncompleted tasks = {percentage_of_incomplete_tasks}\n" \
                           f"Percentage of overdue tasks =  {percentage_of_overdue_tasks}"
    # print(task_overview_string)

    # write task overview into the text file
    with open("task_overview.txt", "w") as overview_file:
        overview_file.write(task_overview_string)


def generate_user_overview(all_tasks_list, all_users):
    # function will create user overview file that displays statistics for all users
    total_number_of_users = len(all_users)
    total_number_of_tasks = len(all_tasks_list)
    report_list_of_strings = [f"User Overview\n{total_number_of_users=}\n{total_number_of_tasks=}\n\n"]

    for participant in all_users:
        num_users_tasks = 0
        total_incomplete = 0
        total_overdue_incomplete_tasks = 0
        for task in all_tasks_list:
            if task["username"] == participant:
                num_users_tasks += 1
                if task["completed"] is False:
                    total_incomplete += 1
                    due_date = task["due_date"]
                    date_today = datetime.today()
                    if due_date < date_today:
                        total_overdue_incomplete_tasks += 1
        # total_user_tasks_completed = num_users_tasks - total_incomplete
        percentage_of_incomplete_tasks = (total_incomplete / total_number_of_tasks) * 100
        percentage_of_completed_user_assigned_tasks = 100 - percentage_of_incomplete_tasks
        percentage_of_overdue_tasks = (total_overdue_incomplete_tasks * 100) / total_number_of_tasks
        percentage_of_user_assigned_tasks = (num_users_tasks * 100) / total_number_of_tasks

        user_overview_string = f"For user {participant}:\n" \
                               f"Number of tasks = {num_users_tasks}\n" \
                               f"Percentage of tasks assigned to user = {percentage_of_user_assigned_tasks}\n" \
                               f"Percentage of completed tasks = {percentage_of_completed_user_assigned_tasks}\n" \
                               f"Percentage of uncompleted tasks = {percentage_of_incomplete_tasks}\n" \
                               f"Percentage of overdue tasks = {percentage_of_overdue_tasks=}\n\n"
        # print(user_overview_string)

        report_list_of_strings.append(user_overview_string)
    report_string = "".join(report_list_of_strings)

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write(report_string)


def get_all_users(user_password_dict):
    # function will return all registered users
    usernames = []
    for registered_user in user_password_dict.keys():
        usernames.append(registered_user)
    return usernames


def generate_reports(all_tasks, username_password_dictionary):
    generate_task_overview(all_tasks)
    generate_user_overview(all_tasks, get_all_users(username_password_dictionary))
    # # generate admin reports
    # task_overview.txt
    # user_overview.txt


def display_stats():
    # function displays statistics using data from user and tasks text files
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    num_users = len(user_data)

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")

    num_tasks = len(task_data)

    print("-----------------------------------")
    print(f"Number of users: \t\t {num_users}")
    print(f"Number of tasks: \t\t {num_tasks}")
    print("-----------------------------------")


def main():
    DATETIME_STRING_FORMAT = "%Y-%m-%d"

    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    add_number_1_to_first_task()

    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    # create dictionary of tasks with key being task number and value all task data
    task_dict = {}

    # create list of tasks, each task to be added as dictionary
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

        task_dict[curr_t['task number']] = curr_t
        task_list.append(curr_t)

    # #====Login Section====
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

        menu_top = '''
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    '''

        menu_bottom = '''
    ds - Display statistics
    e - Exit
    : '''
        menu_admin = "gr - generate reports"

        if curr_user == "admin":
            print(menu_top + menu_admin + menu_bottom)
        else:
            print(menu_top + menu_bottom)

        menu_selection = input("Select one of the following Options above: ").lower()

        if menu_selection == 'r':
            register_new_user(username_password)

        elif menu_selection == 'a':
            add_task(username_password, DATETIME_STRING_FORMAT, task_list)

        elif menu_selection == 'va':
            display_tasks(get_tasks(task_list, None), DATETIME_STRING_FORMAT)

        elif menu_selection == 'vm':
            display_tasks(get_tasks(task_list, user_name=curr_user), DATETIME_STRING_FORMAT)
            user_assigned_tasks_dict = convert_user_assigned_tasks_to_dict(get_tasks(task_list, curr_user))

            while True:
                try:
                    choose_task = input("Enter task number assigned to you or -1 to return to main menu. ")

                    if choose_task == "-1":
                        break
                        # pass
                    elif choose_task in user_assigned_tasks_dict:
                        print(f"You have chosen task number {choose_task}")
                        current_task = user_assigned_tasks_dict[choose_task]
                        amending_task = input("Enter 'edit' to edit the task or MC as mark as completed.  ").lower()
                        if amending_task == "edit":
                            # first check if task marked as True
                            if current_task["completed"] is True:
                                print("The task has been marked as completed and cannot be changed.")
                            else:
                                choose_edit_option = input("Press 1 to edit task owner or press 2 to edit due date. ")
                                if choose_edit_option == "1":
                                    current_task = edit_task_owner(current_task, username_password)
                                    write_tasks_to_file(task_list, DATETIME_STRING_FORMAT)
                                else:
                                    current_task = edit_due_date(current_task, DATETIME_STRING_FORMAT)
                                    write_tasks_to_file(task_list, DATETIME_STRING_FORMAT)
                        # user chooses to mark as complete:
                        elif amending_task == "mc":
                            mark_task_as_complete(task_list, choose_task, DATETIME_STRING_FORMAT)
                            break
                except ValueError:
                    print("You have entered incorrect choice. Only enter positive integers. ")

        elif menu_selection == 'ds' and curr_user == 'admin':
            '''If the user is an admin they can display statistics about number of users
                and tasks.'''
            display_stats()

        # write function to generate reports
        elif menu_selection == 'gr':
            generate_reports(task_list, username_password)


        elif menu_selection == 'e':
            print('Goodbye!!!')
            exit()

        else:
            print("You have made a wrong choice, Please Try again")


if __name__ == "__main__":
    main()

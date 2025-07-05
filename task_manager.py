from datetime import date, datetime
import os

# ======= Helper Functions =======

def load_users():
    users = {}
    try:
        with open("user.txt", "r") as f:
            for line in f:
                if line.strip():
                    username, password = line.strip().split(", ")
                    users[username] = password
    except FileNotFoundError:
        print("user.txt not found. Creating a new one.")
        open("user.txt", "w").close()
    return users

def load_tasks():
    tasks = []
    try:
        with open("tasks.txt", "r") as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split(", ")
                    # expected parts: assigned_user, title, desc, date_assigned, due_date, completed
                    tasks.append(parts)
    except FileNotFoundError:
        print("tasks.txt not found. Creating a new one.")
        open("tasks.txt", "w").close()
    return tasks

def save_tasks(tasks):
    with open("tasks.txt", "w") as f:
        for task in tasks:
            f.write(", ".join(task) + "\n")

def reg_user(users):
    while True:
        new_username = input("Enter new username: ").strip()
        if new_username == "":
            print("Username cannot be empty.")
            continue
        if new_username in users:
            print("Username already exists. Try another.")
            continue
        new_password = input("Enter new password: ").strip()
        confirm_password = input("Confirm password: ").strip()
        if new_password != confirm_password:
            print("Passwords do not match. Try again.")
            continue
        # Save new user
        with open("user.txt", "a") as f:
            f.write(f"\n{new_username}, {new_password}")
        users[new_username] = new_password
        print(f"User '{new_username}' registered successfully!")
        break

def add_task(users):
    assigned_user = input("Enter the username of the person the task is assigned to: ").strip()
    if assigned_user not in users:
        print("This user does not exist. Please enter a valid username.")
        return
    task_title = input("Enter the title of the task: ").strip()
    task_description = input("Enter the description of the task: ").strip()
    due_date = input("Enter the due date of the task (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(due_date, "%Y-%m-%d")  # Validate date format
    except ValueError:
        print("Invalid date format. Please enter date in YYYY-MM-DD format.")
        return
    date_assigned = str(date.today())
    completed = "No"
    with open("tasks.txt", "a") as f:
        f.write(f"\n{assigned_user}, {task_title}, {task_description}, {date_assigned}, {due_date}, {completed}")
    print("Task added successfully.")

def view_all():
    tasks = load_tasks()
    if not tasks:
        print("No tasks to display.")
        return
    for i, task in enumerate(tasks, start=1):
        print("\n" + "-" * 40)
        print(f"Task {i}:")
        print(f"Title:\t\t {task[1]}")
        print(f"Assigned to:\t {task[0]}")
        print(f"Date Assigned:\t {task[3]}")
        print(f"Due Date:\t {task[4]}")
        print(f"Completed:\t {task[5]}")
        print(f"Description:\n{task[2]}")
        print("-" * 40)

def get_valid_task_number(tasks):
    """Recursive function to get a valid task number from user or -1 to exit"""
    try:
        choice = int(input("\nEnter the task number to select or '-1' to return to main menu: "))
        if choice == -1:
            return -1
        elif 1 <= choice <= len(tasks):
            return choice
        else:
            print(f"Invalid input. Please enter a number between 1 and {len(tasks)} or -1.")
            return get_valid_task_number(tasks)
    except ValueError:
        print("Invalid input. Please enter a valid integer.")
        return get_valid_task_number(tasks)

def view_mine(curr_user):
    tasks = load_tasks()
    user_tasks = [task for task in tasks if task[0] == curr_user]
    if not user_tasks:
        print("You have no tasks assigned.")
        return

    while True:
        print("\nYour tasks:")
        for i, task in enumerate(user_tasks, start=1):
            print(f"{i}. {task[1]} (Due: {task[4]}, Completed: {task[5]})")

        choice = get_valid_task_number(user_tasks)
        if choice == -1:
            break

        task = user_tasks[choice - 1]
        print("\nSelected Task:")
        print(f"Title:\t\t {task[1]}")
        print(f"Description:\n{task[2]}")
        print(f"Assigned to:\t {task[0]}")
        print(f"Date Assigned:\t {task[3]}")
        print(f"Due Date:\t {task[4]}")
        print(f"Completed:\t {task[5]}")

        if task[5].lower() == "yes":
            print("\nThis task is already completed and cannot be edited.")
            continue

        action = input("\nSelect action:\n1 - Mark as complete\n2 - Edit task\n3 - Return to task list\nChoose: ").strip()
        if action == "1":
            # Mark as complete
            # Update in tasks list and save
            tasks_index = tasks.index(task)
            tasks[tasks_index][5] = "Yes"
            save_tasks(tasks)
            user_tasks[choice - 1][5] = "Yes"
            print("Task marked as complete.")
        elif action == "2":
            # Edit task: can edit assigned_user or due_date
            new_assigned_user = input(f"Enter new username to assign task (or press Enter to keep '{task[0]}'): ").strip()
            if new_assigned_user:
                users = load_users()
                if new_assigned_user not in users:
                    print("User does not exist. Cannot assign task.")
                    continue
                else:
                    task[0] = new_assigned_user
                    tasks_index = tasks.index(task)
                    tasks[tasks_index][0] = new_assigned_user
            new_due_date = input(f"Enter new due date YYYY-MM-DD (or press Enter to keep '{task[4]}'): ").strip()
            if new_due_date:
                try:
                    datetime.strptime(new_due_date, "%Y-%m-%d")
                    task[4] = new_due_date
                    tasks_index = tasks.index(task)
                    tasks[tasks_index][4] = new_due_date
                except ValueError:
                    print("Invalid date format. Date not changed.")
            save_tasks(tasks)
            print("Task updated.")
        elif action == "3":
            continue
        else:
            print("Invalid choice. Returning to task list.")

def view_completed():
    tasks = load_tasks()
    completed_tasks = [task for task in tasks if task[5].lower() == "yes"]
    if not completed_tasks:
        print("No completed tasks to display.")
        return
    for task in completed_tasks:
        print("\n" + "-" * 40)
        print(f"Task:\t\t {task[1]}")
        print(f"Assigned to:\t {task[0]}")
        print(f"Date Assigned:\t {task[3]}")
        print(f"Due Date:\t {task[4]}")
        print(f"Completed:\t {task[5]}")
        print(f"Description:\n{task[2]}")
        print("-" * 40)

def delete_task():
    tasks = load_tasks()
    if not tasks:
        print("No tasks available to delete.")
        return
    print("\nTasks:")
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task[1]} (Assigned to: {task[0]})")
    try:
        choice = int(input("\nEnter the task number to delete: "))
        if 1 <= choice <= len(tasks):
            deleted_task = tasks.pop(choice - 1)
            save_tasks(tasks)
            print(f"Task '{deleted_task[1]}' deleted successfully.")
        else:
            print("Invalid task number.")
    except ValueError:
        print("Please enter a valid number.")

def generate_reports():
    tasks = load_tasks()
    users = load_users()

    total_tasks = len(tasks)
    completed_tasks = sum(1 for t in tasks if t[5].lower() == "yes")
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = 0
    today = date.today()
    for t in tasks:
        due_date = datetime.strptime(t[4], "%Y-%m-%d").date()
        if t[5].lower() == "no" and due_date < today:
            overdue_tasks += 1
    percent_incomplete = (uncompleted_tasks / total_tasks * 100) if total_tasks else 0
    percent_overdue = (overdue_tasks / total_tasks * 100) if total_tasks else 0

    # Write task_overview.txt
    with open("task_overview.txt", "w") as f:
        f.write(f"Total tasks: {total_tasks}\n")
        f.write(f"Completed tasks: {completed_tasks}\n")
        f.write(f"Uncompleted tasks: {uncompleted_tasks}\n")
        f.write(f"Overdue tasks: {overdue_tasks}\n")
        f.write(f"Percentage incomplete: {percent_incomplete:.2f}%\n")
        f.write(f"Percentage overdue: {percent_overdue:.2f}%\n")

    total_users = len(users)

    # Collect per user stats
    user_task_counts = {user: 0 for user in users}
    user_completed_counts = {user: 0 for user in users}
    user_overdue_counts = {user: 0 for user in users}

    for task in tasks:
        user = task[0]
        if user in users:
            user_task_counts[user] += 1
            if task[5].lower() == "yes":
                user_completed_counts[user] += 1
            else:
                due_date = datetime.strptime(task[4], "%Y-%m-%d").date()
                if due_date < today:
                    user_overdue_counts[user] += 1

    # Write user_overview.txt
    with open("user_overview.txt", "w") as f:
        f.write(f"Total users: {total_users}\n")
        f.write(f"Total tasks: {total_tasks}\n\n")
        for user in users:
            total_user_tasks = user_task_counts[user]
            percent_total = (total_user_tasks / total_tasks * 100) if total_tasks else 0
            completed = user_completed_counts[user]
            incomplete = total_user_tasks - completed
            overdue = user_overdue_counts[user]
            percent_completed = (completed / total_user_tasks * 100) if total_user_tasks else 0
            percent_incomplete_user = (incomplete / total_user_tasks * 100) if total_user_tasks else 0
            percent_overdue_user = (overdue / total_user_tasks * 100) if total_user_tasks else 0

            f.write(f"User: {user}\n")
            f.write(f"  Total tasks assigned: {total_user_tasks}\n")
            f.write(f"  Percentage of total tasks: {percent_total:.2f}%\n")
            f.write(f"  Percentage completed: {percent_completed:.2f}%\n")
            f.write(f"  Percentage incomplete: {percent_incomplete_user:.2f}%\n")
            f.write(f"  Percentage overdue: {percent_overdue_user:.2f}%\n\n")

    print("Reports generated successfully: task_overview.txt and user_overview.txt")

def display_statistics():
    if not (os.path.exists("task_overview.txt") and os.path.exists("user_overview.txt")):
        print("Reports not found. Generating reports first...")
        generate_reports()

    print("\n--- Task Overview ---")
    with open("task_overview.txt", "r") as f:
        print(f.read())

    print("\n--- User Overview ---")
    with open("user_overview.txt", "r") as f:
        print(f.read())

# ======= Main Program =======
def main():
    users = load_users()

    # Login loop
    while True:
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        if username in users and users[username] == password:
            print(f"Welcome {username}!")
            curr_user = username
            break
        else:
            print("Invalid username or password. Please try again.")

    while True:
        if curr_user == "admin":
            menu = input('''\nPlease select one of the following options:
r   - register user
a   - add task
va  - view all tasks
vm  - view my tasks
vc  - view completed tasks
del - delete a task
ds  - display statistics
gr  - generate reports
e   - exit
: ''').lower()
        else:
            menu = input('''\nPlease select one of the following options:
a   - add task
va  - view all tasks
vm  - view my tasks
e   - exit
: ''').lower()

        if menu == "r" and curr_user == "admin":
            reg_user(users)

        elif menu == "a":
            add_task(users)

        elif menu == "va":
            view_all()

        elif menu == "vm":
            view_mine(curr_user)

        elif menu == "vc" and curr_user == "admin":
            view_completed()

        elif menu == "del" and curr_user == "admin":
            delete_task()

        elif menu == "gr" and curr_user == "admin":
            generate_reports()

        elif menu == "ds" and curr_user == "admin":
            display_statistics()

        elif menu == "e":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()

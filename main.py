from functions import list_tasks, add_task, remove_task, edit_task, search_task, field_validation


if __name__ == "__main__":
    welcome_message = """Please, enter command from the list:\n          
    - list (shows all available tasks)
    - add (add a task)
    - remove (remove the task)
    - edit (edit task)
    - search (search tasks)
    - exit (exit the app)
    """
    print(welcome_message)
    while True:
        command = input().strip().lower()
        if command == 'exit':
            print('Good bye!')
            break
        if command not in ["list", "add", "remove", "edit", "search"]:
            print(f"Unknown command.\n {welcome_message}")
        else:
            if command == "list":
                all_tasks = list_tasks()
                if not all_tasks:
                    print('The task list is empty!')
                else:
                    for a_task in all_tasks:
                        print(f'{a_task["id"]}'
                              f' - {a_task["title"]}'                              
                              f' - {a_task["category"]}'
                              f' - {a_task["due_date"]}'
                              f' - {a_task["priority"]}'
                              f' - {a_task["status"]}\n'
                              f'Description: {a_task["description"]}'
                              )

            elif command == "add":
                try:
                    title = input('Please, enter Title: ').strip()
                    field_validation('title', title)
                    description = input('Please, enter Description: ').strip()
                    field_validation('description', description)
                    category = input('Please, enter Category: ').strip()
                    field_validation('category', category)
                    due_date = input('Please, enter Due_date (format YYYY-MM-DD): ').strip()
                    field_validation('due_date', due_date)
                    priority = input('Please, enter Priority (low, medium, high): ').strip()
                    field_validation('priority', priority)
                except ValueError as error_message:
                    print(error_message)
                else:
                    add_task(title, description, category, due_date, priority)
                    print(f'The task {title} with {priority} priority should be done till {due_date}')

            elif command == "remove":
                try:
                    task_id = int(input("Please, enter the task id: ").strip())
                    if remove_task(task_id):
                        print(f"The task with id {task_id} has been removed")
                    else:
                        print(f"There is no task with id {task_id}")
                except ValueError:
                    print('The id should be integer')

            elif command == "edit":
                try:
                    task_id = int(input("Please, enter the task id: ").strip())
                    parameter = input("Please, enter the parameter you wish to edit "
                                          "(title, description, category, due_date, priority, status): "
                                          ).strip()
                    if parameter not in ("title", "description", "category", "due_date", "priority", "status"):
                        raise ValueError("Unknown parameter")
                    new_value = input("Please, enter new value: ").strip()
                    field_validation(parameter, new_value)
                    print(edit_task(task_id, parameter, new_value))
                except ValueError as error_message:
                    print(error_message)

            elif command == "search":
                keywords = input('Please, enter Keywords (or leave empty): ').strip().split()
                category = input('Please, enter Category (or leave empty): ').strip()
                status = input('Please, enter Status (or leave empty): ').strip()
                searched_tasks = search_task(keywords, category, status)
                if not searched_tasks:
                    print('There are no tasks with these criteria')
                else:
                    for a_task in searched_tasks:
                        print(f'{a_task["id"]}'
                              f' - {a_task["title"]}'
                              f' - {a_task["category"]}'
                              f' - {a_task["due_date"]}'
                              f' - {a_task["priority"]}'
                              f' - {a_task["status"]}\n'
                              f'Description: {a_task["description"]}'
                              )

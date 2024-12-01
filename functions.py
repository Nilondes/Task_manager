from datetime import datetime
import json, operator
from functools import reduce


def list_tasks() -> list:
    """Returns a list of dictionaries with keys "id", "title", "description", "category", "due_date", "priority", "status" """
    with open('data.json', 'r') as file:
        tasks = json.load(file)
    return tasks


def add_task(title, description, category, due_date, priority) -> None:
    """Add a new item to task list. The id is determined based on last id or 0 if empty."""
    tasks = list_tasks()
    last_id = 0 if len(tasks) == 0 else tasks[len(tasks) - 1]["id"]
    data = {"id": last_id + 1,
            "title": title,
            "description": description,
            "category": category,
            "due_date": due_date,
            "priority": priority,
            "status": "pending"}
    tasks.append(data)
    with open('data.json', 'w') as file:
        json.dump(tasks, file)


def remove_task(task_id) -> bool:
    """Remove task with specified id or return False if there is no such id in the list"""
    tasks = list_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            with open('data.json', 'w') as file:
                json.dump(tasks, file)
            return True
    return False


def edit_task(task_id, parameter, new_value) -> str:
    """Change task parameter with specified id and new_value or return error message if there is no such id in the list"""
    tasks = list_tasks()
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            current_task = tasks.pop(i)
            current_task[parameter] = new_value
            tasks.insert(i, current_task)
            with open('data.json', 'w') as file:
                json.dump(tasks, file)
            return f'The {parameter} has been changed to {new_value} for task id {task_id}'
    return f'There is no task with id {task_id}'


def search_task(keywords=None, category=None, status=None) -> list:
    """
    Returns a list of dictionaries with keys "id", "title", "description", "category", "due_date", "priority", "status".
    The search is considered as match if all criteria are satisfied.
    Empty criterion is considered as "any"
    """
    tasks = list_tasks()
    result = []
    search_criteria = [['keywords', keywords], ['category', category], ['status', status]]
    for task in tasks:
        for criterion in search_criteria:
            if criterion[0] == 'keywords' and criterion[1]:
                keyword_q = reduce(operator.or_, [keyword in task['title'] or keyword in task['description'] for keyword in keywords])
                if not keyword_q:
                    break
            elif criterion[1] and task[criterion[0]] != criterion[1]:
                break
        else:
            result.append(task)
    return result


def field_validation(field, value) -> None:
    """ Raises ValueError if the field is not valid or returns None """
    if field in ("title", "description", "category") and value == '':
        raise ValueError(f'{field} cannot be blank!')
    elif field == 'due_date':
        try:
            datetime.strptime(value, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('The date should have format YYYY-MM-DD')
    elif field == 'priority' and value not in ('low', 'medium', 'high'):
        raise ValueError('The priority could only be low, medium or high')
    elif field == 'status' and value not in ('pending', 'done'):
        raise ValueError('The status could only be pending or done')
    else:
        return None
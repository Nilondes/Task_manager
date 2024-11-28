import unittest
from main import list_tasks, add_task, remove_task, edit_task, search_task


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.test_task_1 = {"id": 1,
                            "title": "First Task",
                            "description": "Some description",
                            "category": "work",
                            "due_date": "2024-11-28",
                            "priority": "low",
                            "status": "pending"
                            }
        self.test_task_2 = {"id": 2,
                            "title": "Second Task",
                            "description": "Another description",
                            "category": "play",
                            "due_date": "2024-11-28",
                            "priority": "low",
                            "status": "pending"
                            }
        add_task(self.test_task_1["title"],
                 self.test_task_1["description"],
                 self.test_task_1["category"],
                 self.test_task_1["due_date"],
                 self.test_task_1["priority"])
        add_task(self.test_task_2["title"],
                 self.test_task_2["description"],
                 self.test_task_2["category"],
                 self.test_task_2["due_date"],
                 self.test_task_2["priority"])

    def tearDown(self):
        tasks = list_tasks()
        for task in tasks:
            remove_task(task["id"])

    def test_list_tasks(self):
        tasks = list_tasks()
        self.assertEqual(tasks[0], self.test_task_1)
        self.assertEqual(tasks[1], self.test_task_2)

    def test_add_task(self):
        title, description, category, due_date, priority = "Third title", "Third description", "work", "2024-11-29", "medium"
        add_task(title, description, category, due_date, priority)
        tasks = list_tasks()
        self.assertEqual(tasks[2]["id"], 3)

    def test_remove_task(self):
        remove_existing_task = remove_task(1)
        remove_nonexistent_task = remove_task(1)
        tasks = list_tasks()
        self.assertTrue(remove_existing_task)
        self.assertFalse(remove_nonexistent_task)
        self.assertEqual(len(tasks), 1)

    def test_edit_task(self):
        initial_tasks = list_tasks()
        parameter = 'title'
        new_value = 'New title'
        edit_existing_task = edit_task(1, parameter, new_value)
        edit_nonexistent_task = edit_task(7, parameter, new_value)
        edited_tasks = list_tasks()
        self.assertTrue(edit_existing_task, 'The title has been changed to New title for task id 1')
        self.assertEqual(edit_nonexistent_task, 'There is no task with id 7')
        self.assertNotEqual(initial_tasks[0][parameter], edited_tasks[0][parameter])

    def test_search_tasks(self):
        tasks = list_tasks()
        empty_search_tasks = search_task('','','')
        keywords_search_tasks = search_task(('First', 'Another'), '', '')
        category_search_tasks = search_task('', 'work', '')
        status_search_tasks = search_task('', '', 'pending')
        category_and_status_search_tasks = search_task('', 'work', 'done')
        self.assertEqual(empty_search_tasks, tasks)
        self.assertEqual(keywords_search_tasks, tasks)
        self.assertEqual(category_search_tasks[0], tasks[0])
        self.assertEqual(status_search_tasks, tasks)
        self.assertEqual(category_and_status_search_tasks, [])


if __name__ == '__main__':
    unittest.main()
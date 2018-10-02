# project/models.py

class User(object):
    def __init__(self, name, email, password, role):
        self.name = name
        self.email = email
        self.password = password
        self.role = role

    def __repr__(self):
        return '<User {0}>'.format(self.name)

class Task(object):
    def __init__(self, task_description, due_date, priority, posted_date, status, user_id):
        self.name = task_description
        self.due_date = due_date
        self.priority = priority
        self.posted_date = posted_date
        self.status = status
        self.user_id = user_id

    def __repr__(self):
        return '<name {0}'.format(self.name)


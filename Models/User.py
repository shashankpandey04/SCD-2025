from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, registration, first_name, last_name, email, number, company, role):
        self.id = registration
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.number = number
        self.company = company
        self.role = role
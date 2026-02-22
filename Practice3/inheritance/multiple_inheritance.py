class Printer:
    def print_document(self):
        print("Printing document...")

class Scanner:
    def scan_document(self):
        print("Scanning document...")

# Copier inherits from BOTH Printer and Scanner
class Copier(Printer, Scanner):
    def copy(self):
        print("Starting copy process:")
        self.scan_document()
        self.print_document()

office_machine = Copier()
office_machine.copy()

class Father:
    def skills(self):
        print("I can build houses.")

class Mother:
    def skills(self):
        print("I can code in Python.")

# Python looks for methods from left to right (Mother first, then Father)
class Child(Mother, Father):
    pass

tam = Child()
# It will print Mother's skill because 'Mother' is listed first in Child(Mother, Father)
tam.skills()

class JSONExportMixin:
    # A mixin class to add JSON export capability
    def export_to_json(self):
        import json
        return json.dumps(self.__dict__)

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

# Admin inherits the core data from User and the extra feature from the Mixin
class Admin(User, JSONExportMixin):
    pass

admin = Admin("super_admin", "admin@example.com")
print(admin.export_to_json())
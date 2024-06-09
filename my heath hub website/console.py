"""import cmd
import sys
from models import storage
from models.patient import Patient
#from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication

class HealthHubCommand(cmd.Cmd):
    prompt = '(healthhub) '

    def do_quit(self, arg):
        ""Quit command to exit the program""
        return True

    def do_EOF(self, arg):
        ""EOF signal to exit the program""
        print()
        return True

    def emptyline(self):
        ""Do nothing on empty line input""
        pass

"" def do_create(self, arg)
        ""Create a new instance of a model, saves it (ex: create Patient name="John Doe")""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        obj = storage.classes()[class_name]()
        for pair in args[1:]:
            key, value = pair.split("=")
            if value[0] == '"':
                value = value.strip('"').replace('_', ' ')
            setattr(obj, key, value)
        obj.save()
        print(obj.id)""
def do_create(self, arg):
    ""Create a new instance of a model, saves it (ex: create Patient name="John Doe" age=30 medical_history="Some history" contact_info="123-456-7890")""
    args = arg.split()
    if len(args) == 0:
        print("** class name missing **")
        return
    class_name = args[0]
    if class_name not in storage.classes():
        print("** class doesn't exist **")
        return
    obj = storage.classes()[class_name]()
    for pair in args[1:]:
        print("Pair:", pair)
        key, value = pair.split("=")
        if value[0] == '"':
            value = value.strip('"').replace('_', ' ')
        setattr(obj, key, value)
    obj.save()
    print(obj.id)


    def do_show(self, arg):
        ""Show an instance of a model based on class name and id (ex: show Patient 1234)""
        args = arg.split()
        if len(args) < 2:
            print("** class name or id missing **")
            return
        class_name, obj_id = args
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        obj = storage.get(class_name, obj_id)
        if obj is None:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        ""Destroy an instance of a model based on class name and id (ex: destroy Patient 1234)""
        args = arg.split()
        if len(args) < 2:
            print("** class name or id missing **")
            return
        class_name, obj_id = args
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        if not storage.delete(class_name, obj_id):
            print("** no instance found **")
        else:
            storage.save()

    def do_all(self, arg):
        ""Show all instances of a class (ex: all Patient)""
        args = arg.split()
        class_name = args[0] if args else None
        if class_name and class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        objects = storage.all(class_name)
        print([str(obj) for obj in objects.values()])

    def do_update(self, arg):
        ""Update an instance based on class name and id (ex: update Patient 1234 name="Jane Doe")""
        args = arg.split()
        if len(args) < 3:
            print("** class name, id, or attribute missing **")
            return
        class_name, obj_id, attr_name, attr_value = args[0], args[1], args[2], args[3]
        if class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        obj = storage.get(class_name, obj_id)
        if obj is None:
            print("** no instance found **")
            return
        setattr(obj, attr_name, attr_value.strip('"'))
        obj.save()

if __name__ == '__main__':
    HealthHubCommand().cmdloop()
"""


import cmd
from datetime import datetime
from models import db
from models import User, MedicalRecord, Appointment, Department, Payment, Product, Order, OrderItem
from app import app  # Assuming 'app' is defined in app.py or main.py

class HealthHubCommand(cmd.Cmd):
    prompt = '(healthhub) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program"""
        print()
        return True

    def emptyline(self):
        """Do nothing on empty line input"""
        pass

    def do_create(self, arg):
        """Create a new instance of a model, saves it (ex: create User username="JohnDoe" email="john@example.com" ...)"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        cls = globals()[class_name]
        obj_data = {}
        for pair in args[1:]:
            try:
                key, value = pair.split("=")
                if value[0] == '"':
                    value = value.strip('"').replace('_', ' ')
                obj_data[key] = value
            except ValueError:
                print(f"** invalid attribute pair: {pair} **")
                return
        obj = cls(**obj_data)
        db.session.add(obj)
        db.session.commit()
        print(obj)

    def do_show(self, arg):
        """Show an instance of a model based on class name and id (ex: show User 1234)"""
        args = arg.split()
        if len(args) < 2:
            print("** class name or id missing **")
            return
        class_name, obj_id = args
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        cls = globals()[class_name]
        obj = cls.query.get(obj_id)
        if not obj:
            print("** no instance found **")
        else:
            print(obj)

    def do_destroy(self, arg):
        """Destroy an instance of a model based on class name and id (ex: destroy User 1234)"""
        args = arg.split()
        if len(args) < 2:
            print("** class name or id missing **")
            return
        class_name, obj_id = args
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        cls = globals()[class_name]
        obj = cls.query.get(obj_id)
        if not obj:
            print("** no instance found **")
        else:
            db.session.delete(obj)
            db.session.commit()
            print(f"{class_name} {obj_id} deleted")

    def do_all(self, arg):
        """Show all instances of a class (ex: all User)"""
        class_name = arg.strip()
        if class_name and class_name not in globals():
            print("** class doesn't exist **")
            return
        cls = globals()[class_name] if class_name else None
        if cls:
            objects = cls.query.all()
        else:
            objects = []
            for model in [User, MedicalRecord, Appointment, Department, Payment, Product, Order, OrderItem]:
                objects.extend(model.query.all())
        for obj in objects:
            print(obj)

    def do_update(self, arg):
        """Update an instance based on class name and id (ex: update User 1234 username="JaneDoe")"""
        args = arg.split()
        if len(args) < 4:
            print("** class name, id, attribute or value missing **")
            return
        class_name, obj_id, attr_name, attr_value = args[0], args[1], args[2], args[3]
        if class_name not in globals():
            print("** class doesn't exist **")
            return
        cls = globals()[class_name]
        obj = cls.query.get(obj_id)
        if not obj:
            print("** no instance found **")
            return
        try:
            setattr(obj, attr_name, attr_value.strip('"'))
            db.session.commit()
            print(f"{class_name} {obj_id} updated")
        except Exception as e:
            print(f"** error updating instance: {e} **")

if __name__ == '__main__':
    from app import app  # Import the app from your main application file
    with app.app_context():
        HealthHubCommand().cmdloop()

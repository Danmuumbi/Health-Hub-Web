import cmd
import sys
from models import storage
from models.patient import Patient
#from models.doctor import Doctor
from models.appointment import Appointment
from models.medication import Medication

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

""" def do_create(self, arg):
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
        print(obj.id)"""
def do_create(self, arg):
    """Create a new instance of a model, saves it (ex: create Patient name="John Doe" age=30 medical_history="Some history" contact_info="123-456-7890")"""
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
        """Show an instance of a model based on class name and id (ex: show Patient 1234)"""
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
        """Destroy an instance of a model based on class name and id (ex: destroy Patient 1234)"""
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
        """Show all instances of a class (ex: all Patient)"""
        args = arg.split()
        class_name = args[0] if args else None
        if class_name and class_name not in storage.classes():
            print("** class doesn't exist **")
            return
        objects = storage.all(class_name)
        print([str(obj) for obj in objects.values()])

    def do_update(self, arg):
        """Update an instance based on class name and id (ex: update Patient 1234 name="Jane Doe")"""
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

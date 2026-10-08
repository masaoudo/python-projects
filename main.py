import json
from abc import ABC, abstractmethod
from pathlib import Path

database = "school_data.json"
data = {"students": [], "teachers": []}

if Path(database).exists():
    with open(database, 'r') as f:
        data = json.load(f)


def save():
    with open(database, 'w') as f:
        json.dump(data, f, indent=4)


class Person(ABC):
    @abstractmethod
    def get_roles(self):
        pass

    def register(self):
        pass

    def show_details(self):
        pass

    @staticmethod
    def email_verify(email):
        if '@' in email and '.' in email:
            return True
        else:
            return False


class Student(Person):
    def get_roles(self):
        return "student"

    def register(self):
        name = input("enter your name: ")
        age = int(input("enter your age: "))
        email = input("enter your email: ")
        roll_no = int(input("enter your roll no: "))

        if not Person.email_verify(email):
            print("enter a valid email")
            return
        for i in data["students"]:
            if i['roll_no'] == roll_no:
                print("student already exists")
                return
        data['students'].append({
            "name": name,
            "age": age,
            "email": email,
            "roll_no": roll_no,
            "grades": {}
        })
        save()
        print(f"student {name} registered")

    def show_details(self):
        roll_no = int(input("roll no: "))

        for i in data["students"]:
            if i["roll_no"] == roll_no:
                grades = i["grades"]
                avg = sum(grades.values()) / len(grades) if grades else 0

                print(f"\nname : {i['name']}")
                print(f"age : {i['age']}")
                print(f"roll no : {i['roll_no']}")
                print(f"email : {i['email']}")
                print(f"average : {avg:.1f}")

    def add_grades(self):
        roll_no = int(input("roll no: "))
        subject = input("subject: ")
        marks = float(input("marks: "))
        for i in data["students"]:
            if i["roll_no"] == roll_no:
                i["grades"][subject] = marks
                save()
                print("grade added succesfully")
                return

        print("student not found")


class Teacher(Person):
    def get_roles(self):
        return "teacher"

    def register(self):
        name = input("enter your name: ")
        age = int(input("enter your age: "))
        email = input("enter your email: ")
        subject = input("enter your subject: ")
        emp_id = int(input("enter your emp id: "))

        if not Person.email_verify(email):
            print("enter a valid email")
            return

        for i in data["teachers"]:
            if i['emp_id'] == emp_id:
                print("teacher already exists")
                return

        data['teachers'].append({
            "name": name,
            "age": age,
            "email": email,
            "emp_id": emp_id,
            "subject": subject
        })
        save()
        print(f"teacher {name} registered")

    def show_details(self):
        emp_id = int(input("emp_id "))

        for i in data["teachers"]:
            if i["emp_id"] == emp_id:

                print(f"\nname : {i['name']}")
                print(f"age : {i['age']}")
                print(f"emp_id : {i['emp_id']}")
                print(f"email : {i['email']}")
                print(f"age : {i['age']}")


stud = Student()
teac = Teacher()

print("press 1  to register as a student")
print("press 2  to register as a teacher")
print("press 3  to add grades")
print("press 4  to show student details")
print("press 5  to show teacher details")

choice = int(input("please enter your choice: "))

if choice == 1:
    stud.register()
elif choice == 2:
    teac.register()
elif choice == 3:
    stud.add_grades()
elif choice == 4:
    stud.show_details()
elif choice == 5:
    teac.show_details()

import random


def gender(gender_str):
    gender_dict = {
        'm': '♂',
        'f': '♀',
        'o': '⚥'
    }
    return gender_dict[gender_str]


class Student:

    def __init__(self, name, gen):
        self.id = int(random.random() * 10**10)
        self.name = str(name)
        if gen in ("m", "f", "o"):
            self.gender = str(gen)
        else:
            raise ValueError(
                f"Cannot assign '{gen}' as gender. Options are: 'm', 'f', 'o'.")

    def __str__(self):
        return f"{self.name} ({gender(self.gender)})"

    def __repr__(self):
        return f"<Student('{self.name}', '{self.gender}')>"

    def to_json_object(self):
        obj = {
            'name': self.name,
            'gender': self.gender
        }
        return obj

    @staticmethod
    def from_json_object(json: dict):
        student = Student(
            json['name'],
            json['gender']
        )
        return student


class ClassRoom:

    def __init__(self, students=[]):
        self.students = students

    def __str__(self):
        return f"Classroom with students: {', '.join([str(student) for student in self.students])}"

    def __repr__(self):
        return f"<ClassRoom({self.students})>"

    def add_student(self, student: Student):
        self.students.append(student)

    def remove_student(self, student: Student | int | str):
        if isinstance(student, Student):
            self.students = [st for st in self.students if st != student]
        else:
            student_obj = self.get_student(student)
            self.students = [st for st in self.students if st != student_obj]

    def get_student(self, student: int | str):
        if isinstance(student, int):
            student_list = [st for st in self.students if st.id == student]
            if len(student_list) > 1:
                print(
                    f'WARNING! Multiple students found with id {student}:\n {student_list}')
            return student_list[0]
        elif isinstance(student, str):
            student_list = [
                st for st in self.students if student.lower() in st.name.lower()]
            if len(student_list) > 1:
                print(
                    f'WARNING! Multiple students found with name {student}:\n {student_list}')
            return student_list[0]
        else:
            raise TypeError(
                'ClassRoom.get_student() takes either an integer or string as an argument.')

    def to_json_object(self):
        obj = {
            'students': [student.to_json_object() for student in self.students]
        }
        return obj

    @staticmethod
    def from_json_object(json: dict):
        class_room = ClassRoom(
            students=[Student.from_json_object(
                student) for student in json['students']]
        )
        return class_room


class Group:

    def __init__(self, name: str, students: list = []):
        self.name = name
        self.students = students

    def __str__(self):
        return f"Group '{self.name}' with students: {', '.join([str(student) for student in self.students])}"

    def __repr__(self):
        return f"<Group({self.name}, {self.students})>"

    def to_json_object(self):
        obj = {
            'name': self.name,
            'students': [student.to_json_object() for student in self.students]
        }
        return obj

    @staticmethod
    def from_json_object(json: dict):
        group = Group(
            json['name'],
            students=[Student.from_json_object(
                student) for student in json['students']]
        )
        return group

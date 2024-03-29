import random

def gender(gender_str):
    gender_dict = {
        'm': '♂',
        'f': '♀',
        'o': '⚥'
    }
    return gender_dict[gender_str]

class Student:
    
    def __init__(self, name, gender):
        self.id = int(random.random() * 10**10)
        self.name = str(name)
        self.gender = str(gender)

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
        self.students = set(students)

    def __str__(self):
        return f"Classroom with students: {', '.join([str(student) for student in self.students])}"
    
    def __repr__(self):
        return f"<ClassRoom({self.students})>"
    
    def add_student(self, student: Student):
        self.students.add(student)

    def remove_student(self, student: Student|int|str):
        if isinstance(student, Student):
            self.students.remove(student)
        else:
            student_obj = self.get_student(student)
            self.students.remove(student_obj)

    def get_student(self, student: int|str):
        if isinstance(student, int):
            student_list = [st for st in self.students if st.id == student]
            if len(student_list) > 1:
                print(f'WARNING! Multiple students found with id {student}:\n {student_list}')
            return student_list[0]
        elif isinstance(student, str):
            student_list = [st for st in self.students if student.lower() in st.name.lower()]
            if len(student_list) > 1:
                print(f'WARNING! Multiple students found with name {student}:\n {student_list}')
            return student_list[0]
        else:
            raise TypeError('ClassRoom.get_student() takes either an integer or string as an argument.')

    def to_json_object(self):
        obj = {
            'students': [student.to_json_object for student in self.students]
        }
        return obj
    
    @staticmethod
    def from_json_object(json: dict):
        class_room = ClassRoom(
            students = [Student.from_json_object(student) for student in json['students']]
        )
        return class_room

class Group:
    pass
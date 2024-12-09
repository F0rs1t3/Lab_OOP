import pickle
import os
from datetime import datetime

# Save and Load Manager
class SaveManager:
    @staticmethod
    def save_data(filename, data):
        with open(filename, 'wb') as file:
            pickle.dump(data, file)

    @staticmethod
    def load_data(filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as file:
                return pickle.load(file)
        return None

# Logger
class Logger:
    def __init__(self, log_file="system.log"):
        self.log_file = log_file

    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as file:
            file.write(f"[{timestamp}] {message}\n")

# Classes
class University:
    def __init__(self, name):
        self.name = name
        self.faculties = []

    def add_faculty(self, faculty):
        self.faculties.append(faculty)
        logger.log(f"Added faculty: {faculty.name}")

    def find_faculty_by_student(self, student_id):
        for faculty in self.faculties:
            if faculty.has_student(student_id):
                return faculty
        return None

    def display_faculties(self):
        print("University Faculties:")
        for faculty in self.faculties:
            print(faculty.name)

    def display_faculties_by_field(self, field):
        print(f"Faculties in the field '{field}':")
        for faculty in self.faculties:
            if faculty.field == field:
                print(faculty.name)

class Faculty:
    def __init__(self, name, field):
        self.name = name
        self.field = field
        self.students = []
        self.graduates = []

    def add_student(self, student):
        if not self.has_student(student.id):
            self.students.append(student)
            logger.log(f"Added student {student.name} to faculty {self.name}")
        else:
            print(f"Student with ID {student.id} is already in the system.")

    def graduate_student(self, student_id):
        for student in self.students:
            if student.id == student_id:
                self.students.remove(student)
                self.graduates.append(student)
                logger.log(f"Graduated student {student.name} from faculty {self.name}")
                return
        print(f"Cannot graduate student: Student with ID {student_id} not found.")

    def display_enrolled_students(self):
        print(f"Enrolled students in {self.name}:")
        for student in self.students:
            print(f"{student.id}: {student.name}")

    def display_graduates(self):
        print(f"Graduates from {self.name}:")
        for graduate in self.graduates:
            print(f"{graduate.id}: {graduate.name}")

    def has_student(self, student_id):
        return any(student.id == student_id for student in self.students + self.graduates)

class Student:
    def __init__(self, student_id, name, email):
        self.id = student_id
        self.name = name
        self.email = email

# Batch Operations
class BatchProcessor:
    @staticmethod
    def batch_enroll(faculty, filename):
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    student = Student(int(parts[0]), parts[1], parts[2])
                    faculty.add_student(student)

    @staticmethod
    def batch_graduate(faculty, filename):
        if not os.path.exists(filename):
            print(f"File {filename} not found.")
            return
        with open(filename, 'r') as file:
            for line in file:
                student_id = int(line.strip())
                faculty.graduate_student(student_id)

# Initialize
save_file = "university_data.pkl"
logger = Logger()
data = SaveManager.load_data(save_file)
tum = data if data else University("Technical University of Moldova")


# Example Operations
faculty_it = Faculty("Information Technology", "IT")
faculty_gd = Faculty("Game Design", "GD")

def add_faculty_if_not_exists(university, faculty_name, field):
    if not any(faculty.name == faculty_name for faculty in university.faculties):
        university.add_faculty(Faculty(faculty_name, field))
        logger.log(f"Added new faculty: {faculty_name} in field {field}")
        
add_faculty_if_not_exists(tum, "Information Technology", "IT")
add_faculty_if_not_exists(tum, "Game Design", "GD")

# Add and graduate students
student1 = Student(1, "John Doe", "john@example.com")
student2 = Student(2, "Jane Smith", "jane@example.com")
faculty_it.add_student(student1)
faculty_gd.add_student(student2)
faculty_it.graduate_student(1)

# Batch Operations
BatchProcessor.batch_enroll(faculty_it, "batch_enroll.txt")
BatchProcessor.batch_graduate(faculty_it, "batch_graduate.txt")

# Printing to console
faculty_it.display_enrolled_students()
faculty_it.display_graduates()
print("")
tum.display_faculties()
print("")
tum.display_faculties_by_field("IT")

# Save State
SaveManager.save_data(save_file, tum)

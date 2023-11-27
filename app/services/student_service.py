from app.models.db import db
from faker import Faker
from app.models.student_model import Student
from celery import shared_task

fake = Faker()

def generate_fake_student_data(num_students):
    #Generate fake student data.
    student_data = []
    for _ in range(num_students):
        student_data.append({
            "name": fake.name(),
            "age": fake.random_int(min=18, max=30),
            "email": fake.email()
        })

    return student_data

def create_students(student_data):
    try:
        students = [Student(name=data['name'], age=data['age'], email=data['email']) for data in student_data]
        db.session.bulk_save_objects(students)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise e

def get_all_students():
    return Student.query.all()
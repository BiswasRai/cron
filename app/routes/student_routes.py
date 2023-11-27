from flask import Blueprint, request, jsonify
from app.models.db import db
from app.models.user_model import User
from app.services.student_service import generate_fake_student_data, create_students, get_all_students
from app.tasks import celery_add_students

student_bp = Blueprint('students', __name__, url_prefix='/students')

@student_bp.route('/bulk', methods=['POST'])
def create_bulk_students():
    try:
        num_students = request.json.get('num_students', 10)

        success = celery_add_students.delay(num_students)

        if success:
            return jsonify({"message": f"{num_students} fake students created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create fake students"}), 500

    except Exception as e:
        print(e)
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

@student_bp.route('/', methods=['GET'])
def get_students():
    try:
        students = get_all_students()
        print(students)
        students_data = [
            {"id": student.id, "name": student.name, "email": student.email, "age": student.age}
            for student in students
        ]

        return jsonify({"students": students_data})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

from flask import Blueprint, request, jsonify
from app.models.db import db
from app.models.user_model import User
from app.services.user_service import create_user, get_users

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/', methods=['GET'])
def index():
    try:
        users = get_users()
        # Converting list to dictionary for JSON serialization
        user_list = [
            {"id": user.id, "username": user.username, "email": user.email}
            for user in users
        ]

        return jsonify({"users": user_list})
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500


@user_bp.route('/', methods=['POST'])
def create_user_route():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')

        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400

        created_user = create_user(username, email)


        return jsonify({"message": "User created successfully", "user_id": created_user.id}), 201

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

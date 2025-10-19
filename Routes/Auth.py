from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from Models.User import User
from flask_login import login_user, logout_user, login_required, current_user
from Database.mongo import db
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import secrets, string

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
ph = PasswordHasher()

def generate_registration_id():
    prefix = "AWS_SCD25"
    while True:
        suffix = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        reg_id = f"{prefix}-{suffix}"
        if not db.users.find_one({"registration": reg_id}):
            return reg_id

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            return jsonify({
                "status": "error",
                "message": "Email and password are required."
            })

        user_data = db.users.find_one({"email": email})
        if not user_data:
            return jsonify({
                "status": "error",
                "message": "Invalid email or password."
            })

        try:
            ph.verify(user_data['password'], password)
        except VerifyMismatchError:
            return jsonify({
                "status": "error",
                "message": "Invalid email or password."
            })

        user = User(
            registration=user_data['registration'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            number=user_data['number'],
            company=user_data['company'],
            role=user_data['role']
        )
        login_user(user)
        return jsonify({
            "status": "success",
            "message": "Logged in successfully."
        })

    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        number = request.form.get('number')
        company = request.form.get('company')
        role = request.form.get('role')

        if not all([first_name, last_name, email, password, number, company, role]):
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            })

        if db.users.find_one({"email": email}):
            return jsonify({
                "status": "error",
                "message": "Email already registered."
            })

        hashed_password = ph.hash(password)
        registration_id = generate_registration_id()

        user_data = {
            "registration": registration_id,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": hashed_password,
            "number": number,
            "company": company,
            "role": role
        }

        db.users.insert_one(user_data)

        return jsonify({
            "status": "success",
            "message": "Registered successfully. Please log in."
        })

    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html', user=current_user)

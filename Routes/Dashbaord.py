from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from Database.mongo import db
from dotenv import load_dotenv
import os

load_dotenv()

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

EARLY_BIRD_PRICE = float(os.getenv("EARLY_BIRD_PRICE", 99.0))
REGULAR_PRICE = float(os.getenv("REGULAR_PRICE", 149.0))

@dashboard_bp.route('/')
@login_required
def dashboard():
    speakers = db.speaker_waitlist.find({'email': current_user.email})
    sponsor = db.sponsor_waitlist.find_one({'email': current_user.email})
    tickets = db.tickets.find({'email': current_user.email})
    dashboard_data = {
        "speakers": speakers,
        "sponsor": sponsor,
        "tickets": tickets,
        "early_bird_price": EARLY_BIRD_PRICE,
        "regular_price": REGULAR_PRICE
    }
    return render_template('dashboard/dashboard.html', user=current_user, dashboard_data=dashboard_data)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        number = request.form.get('number')
        company = request.form.get('company')
        role = request.form.get('role')

        if not all([first_name, last_name, number, company, role]):
            return jsonify({
                "status": "error",
                "message": "All fields are required."
            })

        db.users.update_one(
            {"email": current_user.email},
            {"$set": {
                "first_name": first_name,
                "last_name": last_name,
                "number": number,
                "company": company,
                "role": role
            }}
        )

        # Update current_user attributes
        current_user.first_name = first_name
        current_user.last_name = last_name
        current_user.number = number
        current_user.company = company
        current_user.role = role

        return jsonify({
            "status": "success",
            "message": "Profile updated successfully."
        })

    return render_template('profile.html', user=current_user)


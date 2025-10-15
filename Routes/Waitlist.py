from flask import Blueprint, render_template, flash, redirect, jsonify, request
from Database.mongo import db

waitlist_bp = Blueprint('waitlist', __name__)

@waitlist_bp.route('/waitlist', methods=['POST','GET'])
def submit_waitlist():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        company = (request.form.get('company') or '').strip()
        role = (request.form.get('role') or '').strip()

        if not (name and email and company and role):
            return jsonify(
                {
                    "error": "Please fill out the form completely."
                }
            )
        
        db.waitlist.insert_one(
            {
                'name': name,
                'email': email,
                'company': company,
                'role': role
            }
        )

        return jsonify(
            {
                "success": "Thank you for joining the waitlist! We will reach out to you soon."
            }
        )


    else:
        return render_template("waitlist.html")
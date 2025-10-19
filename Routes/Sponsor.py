from flask import Blueprint, render_template, flash, redirect, jsonify, request
from flask_login import current_user
from Database.mongo import db

sponsor_bp = Blueprint('sponsor',__name__)

@sponsor_bp.route('/sponsor', methods=['POST','GET'])
def sponsor():
    if request.method == 'POST':
        company = (request.form.get('company') or '').strip()
        contact = (request.form.get('contact') or '').strip()
        email = (request.form.get('email') or '').strip()
        level = (request.form.get('level') or '').strip()
        notes = (request.form.get('notes') or '').strip()

        if not (company and contact and email and level and notes):
            return jsonify(
                {
                    "error": "Please fill out the form completely."
                }
            )

        db.sponsor_waitlist.insert_one(
            {
                'company': company,
                'contact': contact,
                'email': email,
                'level': level,
                'notes': notes
            }
        )

        return jsonify(
            {
                "success": "Thank you for your interest in sponsoring us! We will reach out to you soon."
            }
        )
    else:
        if current_user.is_authenticated:
            existing_sponsor = db.sponsor_waitlist.find_one({'email': current_user.email})
            return render_template('sponsor.html', user=current_user, existing_sponsor=existing_sponsor)
        return render_template('sponsor.html')
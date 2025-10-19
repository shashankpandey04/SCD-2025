from flask import Blueprint, render_template, request, jsonify
from flask_login import current_user
from Database.mongo import db

speaker_bp = Blueprint('speakers',__name__)

@speaker_bp.route('/speakers', methods=['POST','GET'])
def speakers():
    if request.method == 'POST':
        name = (request.form.get('name') or '').strip()
        email = (request.form.get('email') or '').strip()
        title = (request.form.get('title') or '').strip()
        track = (request.form.get('track') or '').strip()
        abstract = (request.form.get('abstract') or '').strip()
        level = (request.form.get('level') or '').strip()
        links = (request.form.get('link') or '').strip()

        if not (name and email and title and track and abstract and level):
            return jsonify({'error': 'Please fill in all required fields for Call for Speakers.'}), 400

        db.speaker_waitlist.insert_one(
            {
                'name': name,
                'email': email,
                'title': title,
                'track': track,
                'abstract': abstract,
                'level': level,
                'links': links,
                'status': 'pending'
            }
        )

        return jsonify(
            {
                'message': 'Thanks for submitting your proposal! We’ll get back to you soon.'
            }
        )
    else:
        if current_user.is_authenticated:
            already_applied = db.speaker_waitlist.find_one({'email': current_user.email})
            return render_template('speaker.html', user=current_user, already_applied=already_applied)
        else:
            return render_template('speaker.html', user=None)
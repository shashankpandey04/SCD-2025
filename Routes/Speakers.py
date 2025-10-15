from flask import Blueprint, render_template, flash, redirect, request, jsonify

from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client['scd']

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
            jsonify({'error': 'Please fill in all required fields for Call for Speakers.'}), 400

        db.speaker_waitlist.insert_one(
            {
                'name': name,
                'email': email,
                'title': title,
                'track': track,
                'abstract': abstract,
                'level': level,
                'links': links
            }
        )

        return jsonify(
            {
                'message': 'Thanks for submitting your proposal! We’ll get back to you soon.'
            }
        )
    else:
        return render_template('speaker.html')
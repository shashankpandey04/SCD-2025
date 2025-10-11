from flask import Flask, render_template, flash, redirect, url_for, request
import csv
from pathlib import Path

app = Flask(__name__)
app.secret_key = "SCD"

@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def error_404(error):
    flash("Looks like you got lost 🤔. We got you to the right track!")
    return redirect('/')


def _write_csv(path: Path, header: list[str], row: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open('a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(header)
        w.writerow(row)


@app.route('/submit-cfs', methods=['POST'])
def submit_cfs():
    name = (request.form.get('name') or '').strip()
    email = (request.form.get('email') or '').strip()
    title = (request.form.get('title') or '').strip()
    track = (request.form.get('track') or '').strip()
    abstract = (request.form.get('abstract') or '').strip()
    level = (request.form.get('level') or '').strip()
    links = (request.form.get('links') or '').strip()

    if not name or not email or not title or not abstract:
        flash('Please fill in all required fields for Call for Speakers.')
        return redirect(url_for('index') + '#cfs')

    data_dir = Path('data')
    _write_csv(
        data_dir / 'call_for_speakers.csv',
        header=['name', 'email', 'title', 'track', 'abstract', 'level', 'links'],
        row=[name, email, title, track, abstract, level, links]
    )
    flash('Thanks for your proposal! We’ll get back to you soon.')
    return redirect(url_for('index') + '#cfs')


@app.route('/submit-sponsor', methods=['POST'])
def submit_sponsor():
    company = (request.form.get('company') or '').strip()
    contact = (request.form.get('contact') or '').strip()
    email = (request.form.get('email') or '').strip()
    level = (request.form.get('level') or '').strip()
    notes = (request.form.get('notes') or '').strip()

    if not company or not contact or not email:
        flash('Please complete the required sponsor fields.')
        return redirect(url_for('index') + '#cfsponsors')

    data_dir = Path('data')
    _write_csv(
        data_dir / 'sponsors.csv',
        header=['company', 'contact', 'email', 'level', 'notes'],
        row=[company, contact, email, level, notes]
    )
    flash('Thanks for your interest in sponsoring! We’ll reach out shortly.')
    return redirect(url_for('index') + '#cfsponsors')

app.run(
    host='0.0.0.0',
    port=80,
    debug=True
)
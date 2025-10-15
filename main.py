from flask import Flask, render_template, flash, redirect, url_for, request
import csv
from pathlib import Path
from dotenv import load_dotenv
import os

from Routes.Sponsor import sponsor_bp
from Routes.Waitlist import waitlist_bp
from Routes.Speakers import speaker_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = "SCD"

app.register_blueprint(sponsor_bp)
app.register_blueprint(waitlist_bp)
app.register_blueprint(speaker_bp)

dynamic_routes = os.getenv("dynamic_routes")
if dynamic_routes:
    try:
        dynamic_routes = eval(dynamic_routes)
        for route, target in dynamic_routes.items():
            app.add_url_rule(f'/{route}', route, lambda target=target: redirect(target))
    except Exception as e:
        print(f"Error setting up dynamic routes: {e}")
        
@app.route('/')
def index():
    return render_template("index.html")

@app.errorhandler(404)
def error_404(error):
    flash("Looks like you got lost 🤔. We got you to the right track!")
    return redirect('/')

app.run(
    host='0.0.0.0',
    port=80,
    debug=True
)

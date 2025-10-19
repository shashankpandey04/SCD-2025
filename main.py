from flask import Flask, render_template, flash, redirect, url_for, request
from Database.mongo import db
from dotenv import load_dotenv
import os

from flask_login import LoginManager

from Routes.Sponsor import sponsor_bp
from Routes.Waitlist import waitlist_bp
from Routes.Speakers import speaker_bp
from Routes.Auth import auth_bp
from Routes.Dashbaord import dashboard_bp

from Models.User import User

load_dotenv()

app = Flask(__name__)
app.secret_key = "SCD"

app.login_manager = LoginManager()
app.login_manager.init_app(app)
app.login_manager.login_view = 'auth.login'

@app.login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"registration": user_id})
    if user_data:
        return User(
            registration=user_data['registration'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            number=user_data['number'],
            company=user_data['company'],
            role=user_data['role'],
            admin=user_data.get('admin', 0)
        )
    return None

routes = [
    sponsor_bp,
    waitlist_bp,
    speaker_bp,
    auth_bp,
    dashboard_bp
]

for route in routes:
    app.register_blueprint(route)

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

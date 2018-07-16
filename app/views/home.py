from flask import Blueprint


home = Blueprint('home', __name__)


@home.route('/')
def dashboard():
    return 'Hello Dashboard'


@home.route('/login')
def login():
    return 'Login Page'


@home.route('/logout')
def logout():
    return 'Logout Page'

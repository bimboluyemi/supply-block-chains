from flask import Blueprint, render_template


home = Blueprint('home', __name__)


@home.route('/')
def dashboard():
    return render_template('home/index.html', title='Dashboard')


@home.route('/login')
def login():
    return 'Login Page'


@home.route('/logout')
def logout():
    return 'Logout Page'

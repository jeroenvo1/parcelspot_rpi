from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION

frontend = Blueprint('frontend', __name__)

@frontend.route('/')
def index():
    return render_template('index.html')
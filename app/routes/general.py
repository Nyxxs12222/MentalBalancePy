from flask import Blueprint, render_template, flash

general_bp = Blueprint('general', __name__)

@general_bp.route('/')
def inicio():
    return render_template('general/inicio.html')
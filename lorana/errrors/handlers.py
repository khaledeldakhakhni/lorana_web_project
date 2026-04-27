from flask import Blueprint, render_template

errors = Blueprint('errors',__name__)

@errors.app_errorhandler(404)  # => when opening page not exist
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)  # => when opening page not allowed
def error_403(error):
    return render_template('errors/403.html'),403

@errors.app_errorhandler(500)  # => when being an error in server (run time error), it's very danger
def error_500(error):
    return render_template('errors/500.html'),500
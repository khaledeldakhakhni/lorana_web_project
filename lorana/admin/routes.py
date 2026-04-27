from flask import Blueprint, url_for, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect
from lorana import db, bcrypt
from lorana.decorators import admin_required
from lorana.modules import User, Product
from lorana.users.forms import Reset_Password

admin = Blueprint('admin',__name__)

@admin.route('/admin_page',methods=['GET','POST'])
@login_required
@admin_required
def admin_page():
    return render_template('admin_page.html',title='admin banal',users =User.query.all(),products = Product.query.all())


@admin.route('/user_admin/<int:user_id>',methods=['POST'])
@login_required
@admin_required
def user_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.is_admin :
        user.is_admin = False
        db.session.commit()
    else:
        user.is_admin = True
        db.session.commit()
    return redirect(url_for('admin.admin_page'))


@admin.route('/del_admin/<int:user_id>',methods=['POST'])
@login_required
@admin_required
def del_admin(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.is_admin = False
    db.session.commit()
    return redirect(url_for('admin.admin_page'))

@admin.route('/change_password/<int:user_id>', methods=['GET','POST'])
@login_required
@admin_required
def change_password(user_id):
    user = User.query.get_or_404(user_id)
    form = Reset_Password()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        return redirect(url_for('admin.admin_page'))
    else:
        return render_template('reset_password.html',form=form)



from flask import Blueprint,render_template, url_for, flash, request
from werkzeug.utils import redirect
from lorana import db, bcrypt
from lorana.users.forms import Register, Login, Edit_Profile , Reset_Request_Form , Reset_Password
from lorana.modules import User, Product
from flask_login import login_user, logout_user, current_user ,login_required

from lorana.users.helpers import send_reset_email

users = Blueprint('users',__name__)

@users.route("/register",methods=['GET','POST'])
def register():
    form = Register()
    user_exist = User.query.filter_by(username=form.username.data).first()
    email_exist = User.query.filter_by(email=form.email.data).first()
    if form.validate_on_submit():
        if user_exist:
            form.username.errors.append('this username already exist')
        elif email_exist :
            form.email.errors.append('this email already exist')
        else :
            hashed_password =bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user=User(fName=form.fName.data ,lName=form.lName.data ,
                      username=form.username.data ,email = form.email.data,password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash(f"User'{form.username.data}'added successfully",'success')
            return redirect(url_for('users.login'))
    return render_template('register.html',form=form)


@users.route("/login",methods=['GET','POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data) :
            login_user(user,remember=form.remember.data) # make a session if user enter remember me
            next_page = request.args.get('next')
            flash(f"You have been logged in",'success')

            if next_page : return redirect(next_page)
            else : return redirect(url_for('main.home'))

        else:
            flash(f"email or password is wrong", 'danger')
    return render_template('login.html',form=form)


@users.route("/logout",methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/profile")
@login_required
def profile():
    return render_template('profile.html',user=current_user)

@users.route("/edit_profile",methods=['GET','POST'])
@login_required
def edit_profile():
    form = Edit_Profile()
    if form.validate_on_submit():
        if form.username.data :
            exist_username = User.query.filter_by(username=form.username.data).first()
            if exist_username:
                form.username.errors.append('this username is already exist')
            else :
                current_user.username = form.username.data
                db.session.commit()
                flash(f"Update success ",'success')
        if form.email.data :
            exist_email = User.query.filter_by(email=form.email.data).first()
            if exist_email:
                form.email.errors.append('this email is already exist')
            else :
                current_user.email = form.email.data
                db.session.commit()
                flash(f"Update success ", 'success')
    return render_template('edit_profile.html',form=form)

@users.route("/reset_request",methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))
    form = Reset_Request_Form()
    if form.validate_on_submit():
        user= User.query.filter_by(email=form.email.data).first()  # => to chick if the email of user is already exist , it return user object
        if user :
            send_reset_email(user)
        flash('Reset request message sent to your emai check your message ', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',title= "reset request" ,form=form)


@users.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated :
        return redirect(url_for('main.home'))

    user = User.verify_reset_token(token)
    if not user:
        flash("the token might be invalid",'warning')
        return redirect(url_for('users.reset_request'))

    form = Reset_Password()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("The Password updated",'success')
        return redirect(url_for('users.login'))
    return render_template('reset_password.html',title= 'reset password', form=form)

@users.route("/favorite/<int:product_id>",methods=['GET','POST'])
def favorite(product_id):
    if current_user.is_authenticated :
        favorite_product = Product.query.filter_by(id=product_id).first()
        if favorite_product:
            if favorite_product in current_user.favorites:
                current_user.favorites.remove(favorite_product)
            else:
                current_user.favorites.append(favorite_product)
            db.session.commit()
        next_page =request.args.get('next')  # next_page => it have thet after word 'next' in url
        if next_page:
            if next_page == 'my_favorite':
                return redirect(url_for('users.my_favorite'))
            return redirect(url_for(next_page))
        return redirect(url_for('main.home'))
    else:
        flash('LogIn to interact with product','info')
        return redirect(url_for('users.login'))

@users.route("/my_favorite")
@login_required
def my_favorite():
    return render_template('my_favorite.html',favorites=current_user.favorites)

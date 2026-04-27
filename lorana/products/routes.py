from flask import Blueprint, render_template, url_for, flash
from flask_login import login_required
from werkzeug.utils import redirect
from lorana import db
from lorana.decorators import admin_required
from lorana.products.forms import AddProduct
from lorana.modules import Product

products = Blueprint('products',__name__)

@products.route("/add", methods=['GET', 'POST'])
@login_required
@admin_required
def add():
    form = AddProduct()
    product_exist = Product.query.filter_by(name=form.name.data).first()
    if form.validate_on_submit():
        if product_exist : form.name.errors.append('this product already exist')
        else:
            new_product = Product(name=form.name.data, price=form.price.data, description=form.desc.data)
            db.session.add(new_product)
            db.session.commit()
            flash(f'Product "{form.name.data}" added successfully', 'success')
            return redirect(url_for('main.home'))
    return render_template('add_product.html', form=form)

@products.route("/delete/<int:id>" ,methods=['POST'])
@login_required
@admin_required
def delete(id):
    deleted = Product.query.get_or_404(id)
    db.session.delete(deleted)
    db.session.commit()
    flash(f'Product "{deleted.name}" deleted successfully', 'danger')
    return redirect(url_for('main.home'))

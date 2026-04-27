from flask import render_template,request, Blueprint
from lorana.modules import Product

main = Blueprint('main',__name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page',1,type=int)
    products = Product.query.paginate(page=page , per_page=4)
    return render_template('home.html', products=products)
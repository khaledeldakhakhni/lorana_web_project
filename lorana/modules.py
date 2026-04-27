from itsdangerous import URLSafeSerializer as Serializer
from flask import current_app
from lorana import db
from flask_login import UserMixin

Favorite = db.Table('favorite',
                     db.Column('user_id', db.Integer, db.ForeignKey('user.id'),primary_key=True),
                     db.Column('product_id',db.Integer ,db.ForeignKey('product.id'),primary_key=True)
                     )

class User(db.Model,UserMixin):
    id       = db.Column(db.Integer , primary_key = True)
    fName    = db.Column(db.String(20),nullable=False)
    lName    = db.Column(db.String(20),nullable=False)
    username = db.Column(db.String(20), unique=True,nullable=False)
    email    = db.Column(db.String(100), unique=True,nullable=False)
    password = db.Column(db.String(150),nullable=False)
    favorites= db.relationship('Product',secondary=Favorite ,backref='favorite_by')
    is_admin = db.Column(db.Boolean , default = False , nullable = False )

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],salt='pw-reset')
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token,age=3600):
        s=Serializer(current_app.config['SECRET_KEY'],salt='pw-reset')
        try:
            user_id = s.loads(token, max_age=age )['user_id']
        except: return None
        return User.query.get(user_id)



class Product(db.Model):
    id          = db.Column(db.Integer,primary_key = True)
    name        = db.Column(db.String(20) , unique = True , nullable = False)
    price       = db.Column(db.String(20)  , nullable = False)
    description = db.Column(db.Text(20) , nullable = False)
    image       = db.Column(db.String(20), unique = False , nullable = False , default = 'default_product.jpg')

from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class AddProduct(FlaskForm):
    name   =StringField('Product Name',validators=[DataRequired(),Length(min=3 , max=20)])
    price  =StringField('Product Price',validators=[DataRequired()])
    desc   =StringField('Description')
    submit =SubmitField('Add Product')
from products.service import get_product_by_id
from flask_wtf import FlaskForm
import decimal
from wtforms import *


class CreateProductCategoryForm(FlaskForm):
    category_name = StringField('Product Category', [validators.DataRequired(), validators.Length(min=1, max=100)])


class CreateProductForm(FlaskForm):
    name = StringField('Product Name', [validators.DataRequired(), validators.Length(min=1, max=100)])
    description = TextAreaField('Product Description',
                                [validators.DataRequired(), validators.Length(min=1, max=1024)])
    price = DecimalField('Product Price', places=2, rounding=decimal.ROUND_UP,
                         validators=[validators.DataRequired(), validators.NumberRange(min=1, max=10000)])
    stock = IntegerField('Product Stock', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    category = SelectField('Product Category', choices=[], validators=[validators.DataRequired()],
                           validate_choice=True)
    is_listed = BooleanField('List Product to Public?', render_kw={'checked': True})


class UpdateProductForm(FlaskForm):
    price = DecimalField('Product Price', places=2, rounding=decimal.ROUND_UP,
                         validators=[validators.DataRequired(), validators.NumberRange(min=1, max=10000)])
    stock = IntegerField('Product Stock', validators=[validators.DataRequired(), validators.NumberRange(min=1)])
    category = SelectField('Product Category', choices=[], validators=[validators.DataRequired()],
                           validate_choice=True)
    is_listed = BooleanField('List Product to Public?', render_kw={'checked': True})


class AddProductToCartForm(FlaskForm):
    product_id = HiddenField("Product ID", validators=[validators.DataRequired(), validators.NumberRange()])
    item_count = IntegerField("Quantity", validators=[validators.DataRequired(), validators.NumberRange(min=1)], default=1)

    def validate(self, extra_validators=None):
        # Check initial validation of field input
        initial_validation = super(AddProductToCartForm, self).validate()
        if not initial_validation:
            return False
        product = get_product_by_id(self.product_id.data)
        # Return an error if product has no more stock
        if product.stock < 1:
            self.item_count.errors.append("There is currently no stock for this product!")
            return False
        # Return an error if purchase quantity is greater than product stock available
        if product.stock < self.item_count.data:
            self.item_count.errors.append("You cannot purchase more than the available stock! "
                                          "Please reload this page if you are seeing outdated stock.")
            return False
        return True

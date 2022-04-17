from flask_wtf import FlaskForm
from products.service import get_product_by_id
from wtforms import *


class UpdateCartItem(FlaskForm):
    product_id = HiddenField("Product ID", validators=[validators.DataRequired(), validators.NumberRange()])
    item_count = IntegerField("Quantity", validators=[validators.DataRequired(), validators.NumberRange(min=1)],
                              default=1)

    def validate(self, extra_validators=None):
        # Check initial validation of field input
        initial_validation = super(UpdateCartItem, self).validate()
        if not initial_validation:
            return False
        product = get_product_by_id(self.product_id.data)
        # Return an error if the product has no more stock
        if product.stock < 1:
            self.item_count.errors.append("There is currently no stock for this product!")
            return False
        # Return an error if the purchase quantity is greater than stock available
        if product.stock < self.item_count.data:
            self.item_count.errors.append("You cannot purchase more than the available stock! "
                                          "Please reload this page if you are seeing outdated stock.")
            return False
        return True


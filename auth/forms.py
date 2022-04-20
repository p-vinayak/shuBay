from users.service import get_user_by_email, get_user_by_id
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import *


PHONE_NUMBER_VALIDATION_REGEX = '^\s*(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\s*$'


# Checks if email is already registered
def is_email_registered(form, field):
    if get_user_by_email(field.data) is not None:
        raise ValidationError("Email already registered")


class RegistrationForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired(), is_email_registered])
    first_name = StringField('First Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    last_name = StringField('Last Name', [validators.Length(min=1, max=50), validators.DataRequired()])
    phone_number = StringField('Phone Number', [validators.Length(min=10, max=20),
                                                validators.DataRequired(),
                                                validators.Regexp(PHONE_NUMBER_VALIDATION_REGEX,
                                                                  message="Must be a valid phone number")])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.EqualTo('password_confirm', message="Passwords must match"),
                                          validators.Length(min=6, max=128)])
    password_confirm = PasswordField('Confirm Password', [validators.DataRequired()])


class LoginForm(FlaskForm):
    email = EmailField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])

    def validate(self, extra_validators=None):
        # Check initial validation of field input
        initial_validation = super(LoginForm, self).validate()
        if not initial_validation:
            return False
        user = get_user_by_email(self.email.data)
        # Check if entered email is a registered users
        if user is None:
            self.email.errors.append("Email not registered")
            return False
        # Check if passwords match
        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append("Passwords did not match")
            return False
        return True


class UpdatePasswordForm(FlaskForm):
    user_id = HiddenField("User ID", validators=[validators.DataRequired(), validators.NumberRange()])
    old_password = PasswordField('Old Password')
    new_password = PasswordField('New Password', [validators.DataRequired(),
                                                  validators.EqualTo('new_password_confirm', message="Passwords must match"),
                                                  validators.Length(min=6, max=128)])
    new_password_confirm = PasswordField('Confirm New Password', [validators.DataRequired()])

    def validate(self, extra_validators=None):
        # Check initial validation of field input
        initial_validation = super(UpdatePasswordForm, self).validate()
        if not initial_validation:
            return False
        user = get_user_by_id(self.user_id.data)
        # Check if entered email is a registered users
        if user is None:
            self.user_id.errors.append("User does not exist")
            return False
        # Check old password is correct
        if not check_password_hash(user.password, self.old_password.data):
            self.old_password.errors.append("Incorrect password")
            return False
        return True

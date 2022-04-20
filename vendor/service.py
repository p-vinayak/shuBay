from users.models import User
from vendor.models import VendorApplication
from products.models import Product
from datetime import datetime
from db import db


# Gets all vendors
def get_all_vendors():
    return User.query.filter_by(is_vendor=True).all()


# Gets incomplete application for a user
def get_active_application_for_user(user_id):
    return VendorApplication.query.filter_by(owner_id=user_id, is_active=True).first()


# Creates a vendor application
def create_vendor_application(owner_id, title, description):
    new_application = VendorApplication(owner_id, title, description)
    db.session.add(new_application)
    db.session.commit()


# Gets all incomplete applications
def get_all_active_applications():
    return VendorApplication.query.filter_by(is_active=True).all()


# Gets specific application by id
def get_application_by_id(application_id):
    return VendorApplication.query.filter_by(id=application_id).first()


# Completes an application
def complete_application(application_id, approval, completed_by_id):
    application = VendorApplication.query.filter_by(id=application_id).first()
    application.approved = approval
    application.completed_by_id = completed_by_id
    application.completed_at = datetime.utcnow()
    application.is_complete = True
    application.is_active = False
    application.owner.is_vendor = approval
    db.session.commit()

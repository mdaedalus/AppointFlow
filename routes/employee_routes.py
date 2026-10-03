from flask import Blueprint, render_template, redirect, url_for
from models import Business, Employee

employee_bp = Blueprint('employee', __name__)


@employee_bp.route('/')
def dashboard():
    business = Business.query.first()
    if not business:
        return redirect(url_for('setup.step1'))
    employees = Employee.query.filter_by(business_id=business.id).all()
    return render_template('employee/dashboard.html', business=business, employees=employees)
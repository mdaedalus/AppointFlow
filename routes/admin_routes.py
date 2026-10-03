from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from database import db
from models import Business, Service, Employee, Appointment, CalendarIntegration
from datetime import datetime

admin_bp = Blueprint('admin', __name__)


def get_business():
    return Business.query.first()


@admin_bp.route('/')
def dashboard():
    business = get_business()
    if not business:
        return redirect(url_for('setup.step1'))
    return redirect(url_for('admin.calendar_view'))


@admin_bp.route('/services')
def services_page():
    business = get_business()
    if not business:
        return redirect(url_for('setup.step1'))
    services = Service.query.filter_by(business_id=business.id).all()
    return render_template('admin/services.html', business=business, services=services)


@admin_bp.route('/services/add', methods=['POST'])
def add_service():
    business = get_business()
    data = request.get_json()
    service = Service(
        business_id=business.id,
        name=data['name'],
        price=float(data['price']) if data.get('price') else None,
        duration=int(data.get('duration', 30))
    )
    db.session.add(service)
    db.session.commit()
    return jsonify({'success': True, 'id': service.id})


@admin_bp.route('/services/<int:sid>', methods=['PUT'])
def update_service(sid):
    service = Service.query.get_or_404(sid)
    data = request.get_json()
    service.name = data.get('name', service.name)
    if data.get('price') is not None:
        service.price = float(data['price']) if data['price'] != '' else None
    if data.get('duration'):
        service.duration = int(data['duration'])
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/services/<int:sid>', methods=['DELETE'])
def delete_service(sid):
    service = Service.query.get_or_404(sid)
    db.session.delete(service)
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/employees')
def employees_page():
    business = get_business()
    employees = Employee.query.filter_by(business_id=business.id).all()
    return render_template('admin/employees.html', business=business, employees=employees)


@admin_bp.route('/employees/add', methods=['POST'])
def add_employee():
    business = get_business()
    data = request.get_json()
    emp = Employee(
        business_id=business.id,
        name=data['name'],
        phone=data['phone']
    )
    db.session.add(emp)
    db.session.commit()
    return jsonify({'success': True, 'id': emp.id})


@admin_bp.route('/employees/<int:eid>', methods=['PUT'])
def update_employee(eid):
    emp = Employee.query.get_or_404(eid)
    data = request.get_json()
    emp.name = data.get('name', emp.name)
    emp.phone = data.get('phone', emp.phone)
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/employees/<int:eid>', methods=['DELETE'])
def delete_employee(eid):
    emp = Employee.query.get_or_404(eid)
    db.session.delete(emp)
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/calendar')
def calendar_view():
    business = get_business()
    return render_template('admin/calendar_view.html', business=business)


@admin_bp.route('/appointments')
def appointments_page():
    business = get_business()
    services = Service.query.filter_by(business_id=business.id).all()
    employees = Employee.query.filter_by(business_id=business.id, is_active=True).all()
    return render_template('admin/appointments.html',
                           business=business,
                           services=services,
                           employees=employees)


@admin_bp.route('/calendar-integration')
def calendar_integration_page():
    business = get_business()
    integrations = CalendarIntegration.query.filter_by(business_id=business.id).all()
    return render_template('admin/calendar_integration.html',
                           business=business,
                           integrations=integrations)


@admin_bp.route('/calendar-integration/add', methods=['POST'])
def add_calendar_integration():
    business = get_business()
    data = request.get_json()
    integration = CalendarIntegration(
        business_id=business.id,
        provider=data.get('provider'),
        email=data.get('email'),
        calendar_url=data.get('calendar_url')
    )
    db.session.add(integration)
    db.session.commit()
    return jsonify({'success': True})


@admin_bp.route('/calendar-integration/<int:iid>', methods=['DELETE'])
def delete_calendar_integration(iid):
    integration = CalendarIntegration.query.get_or_404(iid)
    db.session.delete(integration)
    db.session.commit()
    return jsonify({'success': True})
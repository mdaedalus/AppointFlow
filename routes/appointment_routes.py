from flask import Blueprint, request, jsonify, redirect, url_for
from database import db
from models import Business, Service, Employee, Appointment, AppointmentService, AppointmentEmployee
from datetime import datetime

appointment_bp = Blueprint('appointment', __name__)


@appointment_bp.route('/create', methods=['POST'])
def create_appointment():
    business = Business.query.first()
    if not business:
        return jsonify({'success': False, 'message': 'İşletme yok'}), 400

    data = request.get_json()

    try:
        appt_date = datetime.strptime(data['appointment_date'], '%Y-%m-%dT%H:%M')
    except Exception:
        return jsonify({'success': False, 'message': 'Geçersiz tarih'}), 400

    service_ids = data.get('service_ids', [])
    employee_ids = data.get('employee_ids', [])

    if not service_ids:
        return jsonify({'success': False, 'message': 'En az bir işlem seçin'}), 400
    if not employee_ids:
        return jsonify({'success': False, 'message': 'En az bir çalışan seçin'}), 400

    # Toplam fiyat
    total = 0
    services = Service.query.filter(Service.id.in_(service_ids)).all()
    for s in services:
        if s.price:
            total += s.price

    appt = Appointment(
        business_id=business.id,
        customer_name=data['customer_name'],
        customer_phone=data['customer_phone'],
        appointment_date=appt_date,
        description=data.get('description', ''),
        total_price=total,
        status='pending'
    )
    db.session.add(appt)
    db.session.flush()

    for sid in service_ids:
        db.session.add(AppointmentService(appointment_id=appt.id, service_id=sid))
    for eid in employee_ids:
        db.session.add(AppointmentEmployee(appointment_id=appt.id, employee_id=eid))

    db.session.commit()

    return jsonify({
        'success': True,
        'appointment_id': appt.id,
        'message': 'Randevu oluşturuldu'
    })


@appointment_bp.route('/list', methods=['GET'])
def list_appointments():
    business = Business.query.first()
    if not business:
        return jsonify({'appointments': []})

    appts = Appointment.query.filter_by(business_id=business.id).order_by(Appointment.appointment_date).all()

    result = []
    for a in appts:
        service_names = [s.service.name for s in a.services if s.service]
        employee_names = [e.employee.name for e in a.employees if e.employee]
        result.append({
            'id': a.id,
            'customer_name': a.customer_name,
            'customer_phone': a.customer_phone,
            'appointment_date': a.appointment_date.isoformat(),
            'description': a.description,
            'total_price': a.total_price,
            'status': a.status,
            'services': service_names,
            'employees': employee_names
        })

    return jsonify({'appointments': result})


@appointment_bp.route('/<int:aid>', methods=['GET'])
def get_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    return jsonify({
        'id': a.id,
        'customer_name': a.customer_name,
        'customer_phone': a.customer_phone,
        'appointment_date': a.appointment_date.strftime('%Y-%m-%dT%H:%M'),
        'description': a.description,
        'total_price': a.total_price,
        'status': a.status,
        'service_ids': [s.service_id for s in a.services],
        'employee_ids': [e.employee_id for e in a.employees]
    })


@appointment_bp.route('/<int:aid>', methods=['PUT'])
def update_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    data = request.get_json()

    a.customer_name = data.get('customer_name', a.customer_name)
    a.customer_phone = data.get('customer_phone', a.customer_phone)
    if data.get('appointment_date'):
        a.appointment_date = datetime.strptime(data['appointment_date'], '%Y-%m-%dT%H:%M')
    a.description = data.get('description', a.description)

    if 'service_ids' in data:
        AppointmentService.query.filter_by(appointment_id=a.id).delete()
        total = 0
        for sid in data['service_ids']:
            db.session.add(AppointmentService(appointment_id=a.id, service_id=sid))
            s = Service.query.get(sid)
            if s and s.price:
                total += s.price
        a.total_price = total

    if 'employee_ids' in data:
        AppointmentEmployee.query.filter_by(appointment_id=a.id).delete()
        for eid in data['employee_ids']:
            db.session.add(AppointmentEmployee(appointment_id=a.id, employee_id=eid))

    db.session.commit()
    return jsonify({'success': True})


@appointment_bp.route('/<int:aid>', methods=['DELETE'])
def delete_appointment(aid):
    a = Appointment.query.get_or_404(aid)
    db.session.delete(a)
    db.session.commit()
    return jsonify({'success': True})


@appointment_bp.route('/<int:aid>/status', methods=['PUT'])
def update_status(aid):
    a = Appointment.query.get_or_404(aid)
    data = request.get_json()
    status = data.get('status')
    if status not in ['pending', 'arrived', 'no_show']:
        return jsonify({'success': False, 'message': 'Geçersiz durum'}), 400
    a.status = status
    db.session.commit()
    return jsonify({'success': True})


@appointment_bp.route('/<int:aid>/ics')
def download_ics(aid):
    """Takvim dosyası (.ics) üret"""
    from services.calendar_service import generate_ics
    from flask import Response
    a = Appointment.query.get_or_404(aid)
    business = Business.query.first()
    ics_content = generate_ics(a, business)
    return Response(
        ics_content,
        mimetype='text/calendar',
        headers={'Content-Disposition': f'attachment; filename=randevu_{aid}.ics'}
    )
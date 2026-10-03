from flask import Blueprint, jsonify
from models import Business, Appointment, Service, Employee

calendar_bp = Blueprint('calendar', __name__)


@calendar_bp.route('/events', methods=['GET'])
def events():
    """FullCalendar için event listesi"""
    business = Business.query.first()
    if not business:
        return jsonify([])

    appts = Appointment.query.filter_by(business_id=business.id).all()

    colors = {
        'pending': '#6366f1',
        'arrived': '#10b981',
        'no_show': '#ef4444'
    }

    events = []
    for a in appts:
        service_names = ", ".join([s.service.name for s in a.services if s.service])
        employee_names = ", ".join([e.employee.name for e in a.employees if e.employee])
        events.append({
            'id': a.id,
            'title': f"{a.customer_name} - {service_names}",
            'start': a.appointment_date.isoformat(),
            'backgroundColor': colors.get(a.status, '#6366f1'),
            'borderColor': colors.get(a.status, '#6366f1'),
            'extendedProps': {
                'customer_phone': a.customer_phone,
                'employees': employee_names,
                'description': a.description,
                'status': a.status,
                'total_price': a.total_price
            }
        })

    return jsonify(events)
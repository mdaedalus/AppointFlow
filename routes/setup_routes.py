from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from database import db
from models import Business, Service, Employee

setup_bp = Blueprint('setup', __name__)


def business_exists():
    return Business.query.first() is not None


@setup_bp.route('/')
def index():
    """İlk açılışta işletme oluşturma ekranı"""
    if business_exists():
        return redirect(url_for('admin.dashboard'))
    return redirect(url_for('setup.step1'))


@setup_bp.route('/setup/step1')
def step1():
    if business_exists():
        return redirect(url_for('admin.dashboard'))
    return render_template('setup/step1_business.html')


@setup_bp.route('/setup/step1', methods=['POST'])
def step1_save():
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'success': False, 'message': 'İşletme adı gerekli'}), 400

    # Oturumda sakla (business henüz oluşturulmadı)
    from flask import session
    session['setup_business_name'] = name
    return jsonify({'success': True})


@setup_bp.route('/setup/step2')
def step2():
    if business_exists():
        return redirect(url_for('admin.dashboard'))
    return render_template('setup/step2_services.html')


@setup_bp.route('/setup/step2', methods=['POST'])
def step2_save():
    from flask import session
    data = request.get_json()
    services = data.get('services', [])
    has_pricing = data.get('has_pricing', False)

    session['setup_services'] = services
    session['setup_has_pricing'] = has_pricing
    return jsonify({'success': True})


@setup_bp.route('/setup/step3')
def step3():
    if business_exists():
        return redirect(url_for('admin.dashboard'))
    return render_template('setup/step3_employees.html')


@setup_bp.route('/setup/step3', methods=['POST'])
def step3_save():
    from flask import session
    data = request.get_json()
    employees = data.get('employees', [])

    business_name = session.get('setup_business_name')
    services = session.get('setup_services', [])
    has_pricing = session.get('setup_has_pricing', False)

    if not business_name:
        return jsonify({'success': False, 'message': 'Önceki adımlar tamamlanmadı'}), 400

    # İşletme oluştur
    business = Business(name=business_name, has_pricing=has_pricing)
    db.session.add(business)
    db.session.flush()

    # Hizmetleri kaydet
    for s in services:
        service = Service(
            business_id=business.id,
            name=s.get('name'),
            price=float(s.get('price') or 0) if has_pricing else None,
            duration=int(s.get('duration') or 30)
        )
        db.session.add(service)

    # Çalışanları kaydet
    for e in employees:
        emp = Employee(
            business_id=business.id,
            name=e.get('name'),
            phone=e.get('phone')
        )
        db.session.add(emp)

    db.session.commit()

    # Session temizle
    session.pop('setup_business_name', None)
    session.pop('setup_services', None)
    session.pop('setup_has_pricing', None)

    return jsonify({'success': True, 'redirect': url_for('admin.dashboard')})
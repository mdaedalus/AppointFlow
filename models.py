from datetime import datetime
from database import db


class Business(db.Model):
    """İşletme modeli - sistem başına 1 tane olur"""
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    has_pricing = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship('Service', backref='business', cascade='all, delete-orphan')
    employees = db.relationship('Employee', backref='business', cascade='all, delete-orphan')
    appointments = db.relationship('Appointment', backref='business', cascade='all, delete-orphan')


class Service(db.Model):
    """İşlem/Hizmet modeli"""
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=True)
    duration = db.Column(db.Integer, default=30)  # dakika


class Employee(db.Model):
    """Çalışan modeli"""
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    is_active = db.Column(db.Boolean, default=True)


class Appointment(db.Model):
    """Randevu modeli"""
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    customer_name = db.Column(db.String(150), nullable=False)
    customer_phone = db.Column(db.String(30), nullable=False)
    appointment_date = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    total_price = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')  # pending, arrived, no_show
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    services = db.relationship('AppointmentService', backref='appointment', cascade='all, delete-orphan')
    employees = db.relationship('AppointmentEmployee', backref='appointment', cascade='all, delete-orphan')


class AppointmentService(db.Model):
    __tablename__ = 'appointment_services'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    service = db.relationship('Service')


class AppointmentEmployee(db.Model):
    __tablename__ = 'appointment_employees'
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    employee = db.relationship('Employee')


class CalendarIntegration(db.Model):
    """Takvim entegrasyon ayarları"""
    __tablename__ = 'calendar_integrations'
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    provider = db.Column(db.String(50))  # google, icloud, outlook
    email = db.Column(db.String(150))
    calendar_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
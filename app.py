import os
from flask import Flask
from config import Config
from database import db

# Route modüllerini içe aktar
from routes.setup_routes import setup_bp
from routes.admin_routes import admin_bp
from routes.employee_routes import employee_bp
from routes.appointment_routes import appointment_bp
from routes.calendar_routes import calendar_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # instance klasörünü oluştur
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)

    db.init_app(app)

    # Blueprint kayıtları
    app.register_blueprint(setup_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(employee_bp, url_prefix='/employee')
    app.register_blueprint(appointment_bp, url_prefix='/appointment')
    app.register_blueprint(calendar_bp, url_prefix='/calendar')

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=8000)
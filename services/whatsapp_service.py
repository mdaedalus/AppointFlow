from urllib.parse import quote
from flask import Blueprint, jsonify

wa_bp = Blueprint('whatsapp', __name__)


def build_whatsapp_url(phone, message):
    """
    WhatsApp Desktop/Web için URL üretir.
    Kullanıcı bu linke tıkladığında bilgisayardaki WhatsApp uygulaması açılır.
    """
    phone_clean = ''.join(filter(str.isdigit, phone))
    if phone_clean.startswith('0'):
        phone_clean = '90' + phone_clean[1:]
    elif not phone_clean.startswith('90'):
        phone_clean = '90' + phone_clean

    return f"https://wa.me/{phone_clean}?text={quote(message)}"


def build_default_message(customer_name, appointment_date, service_names, business_name):
    return (
        f"Merhaba {customer_name},\n\n"
        f"{business_name} işletmesinden randevunuz oluşturulmuştur.\n\n"
        f"📅 Tarih: {appointment_date}\n"
        f"✂️ İşlem: {service_names}\n\n"
        f"Randevunuza zamanında gelmenizi rica ederiz.\n"
        f"Değişiklik için bize ulaşabilirsiniz."
    )
from datetime import timedelta


def generate_ics(appointment, business):
    """ICS (iCalendar) formatında takvim dosyası üretir"""
    start = appointment.appointment_date
    duration = 60  # varsayılan 1 saat
    end = start + timedelta(minutes=duration)

    service_names = ", ".join([s.service.name for s in appointment.services if s.service])
    employee_names = ", ".join([e.employee.name for e in appointment.employees if e.employee])

    description = appointment.description or ""
    description += f"\\nHizmet: {service_names}\\nPersonel: {employee_names}"
    if appointment.total_price:
        description += f"\\nÜcret: {appointment.total_price} TL"

    dt_start = start.strftime('%Y%m%dT%H%M%S')
    dt_end = end.strftime('%Y%m%dT%H%M%S')

    ics = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Randevu Sistemi//TR
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
UID:{appointment.id}@randevu-sistemi
DTSTAMP:{dt_start}
DTSTART:{dt_start}
DTEND:{dt_end}
SUMMARY:{business.name} - {appointment.customer_name}
DESCRIPTION:{description}
LOCATION:{business.name}
STATUS:CONFIRMED
BEGIN:VALARM
TRIGGER:-PT30M
ACTION:DISPLAY
DESCRIPTION:Randevu Hatırlatma
END:VALARM
END:VEVENT
END:VCALENDAR"""

    return ics
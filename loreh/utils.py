# utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_booking_emails(appointment, deposit_amount):
    subject = "New Booking Received"
    message = f"""
New booking received:

Name: {appointment.name}
Email: {appointment.email}
Phone: {appointment.phone}
Service: {appointment.service.name}
Subservice: {appointment.subservice.name if appointment.subservice else "N/A"}
Date: {appointment.date}
Time: {appointment.time}
Notes: {appointment.notes}
Deposit Paid: ₦{deposit_amount}
"""

    # Send to admin
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        ["tejiriacho62@email.com"],  # replace with your email
    )

    # Send confirmation to customer
    send_mail(
        "Your Booking is Confirmed",
        f"Dear {appointment.name},\n\nYour booking for {appointment.service.name} "
        f"({appointment.subservice.name if appointment.subservice else ''}) on {appointment.date} at {appointment.time} "
        f"has been confirmed.\nDeposit Paid: ₦{deposit_amount}\n\nThank you!",
        settings.DEFAULT_FROM_EMAIL,
        [appointment.email],
    )

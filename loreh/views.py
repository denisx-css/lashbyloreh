from django.shortcuts import render, redirect, get_object_or_404
from .models import Service, Page, Appointment, SubService
from .forms import ContactForm, AppointmentForm
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from .paystack import Paystack
import uuid




def index(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            deposit_amount = appointment.price * Decimal("0.4")

            # ✅ Generate unique reference
            reference = str(uuid.uuid4())
            appointment.paystack_ref = reference
            appointment.save()

            # ✅ Initialize Paystack payment
            paystack = Paystack()
            callback_url = request.build_absolute_uri(
                f"/verify-payment/{appointment.id}/"
            )
            response = paystack.initialize_payment(
                appointment.email, deposit_amount, reference, callback_url
            )

            if response["status"]:
                auth_url = response["data"]["authorization_url"]
                return redirect(auth_url)
            else:
                return HttpResponse("Error initializing payment", status=400)
    else:
        form = AppointmentForm()
    return render(request, "index.html", {"form": form})


def verify_payment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    paystack = Paystack()
    response = paystack.verify_payment(appointment.paystack_ref)

    if response["status"] and response["data"]["status"] == "success":
        appointment.paid = True
        appointment.save()

        deposit_amount = appointment.price * Decimal("0.4")
        deposit_amount_str = f"₦{deposit_amount:,.2f}"

        # ✅ Send admin email
        subject = f"New Appointment – {appointment.service.name}"
        html_content = f"""
        <h2>New Booking Received</h2>
        <p><strong>Name:</strong> {appointment.name}</p>
        <p><strong>Email:</strong> {appointment.email}</p>
        <p><strong>Phone:</strong> {appointment.phone}</p>
        <p><strong>Service:</strong> {appointment.service}</p>
        <p><strong>Subservice:</strong> {appointment.subservice or 'Not selected'}</p>
        <p><strong>Date:</strong> {appointment.date}</p>
        <p><strong>Time:</strong> {appointment.time}</p>
        <p><strong>Notes:</strong> {appointment.notes or 'None'}</p>
        <p><strong>Deposit:</strong> {deposit_amount_str}</p>
        """
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, None, ["tejiriacho62@gmail.com"])
        email.attach_alternative(html_content, "text/html")
        email.send()

        # ✅ Send client confirmation
        subject = "Your Booking Confirmation"
        html_content = f"""
        <h2>Thank you for booking with us, {appointment.name}!</h2>
        <p>Your appointment has been confirmed:</p>
        <ul>
          <li><strong>Service:</strong> {appointment.service}</li>
          <li><strong>Subservice:</strong> {appointment.subservice or 'Not selected'}</li>
          <li><strong>Date:</strong> {appointment.date}</li>
          <li><strong>Time:</strong> {appointment.time}</li>
          <li><strong>Deposit:</strong> {deposit_amount_str}</li>
        </ul>
        <p>We look forward to seeing you!</p>
        <p>Best regards,<br/>Team LorehLuxe</p>
        """
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(subject, text_content, None, [appointment.email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        return render(
            request,
            "booking_success.html",
            {"appointment": appointment, "deposit_amount": deposit_amount},
        )
    else:
        return HttpResponse("Payment Failed", status=400)
    


def services(request):
    services = Service.objects.all()
    return render(request, "services.html", {"services": services})


def load_subservices(request):
    service_id = request.GET.get("service")
    subservices = SubService.objects.filter(service_id=service_id).values("id", "name")
    return JsonResponse(list(subservices), safe=False)


def testimonials(request):
    return render(request, "testimonials.html")


def page_about(request):
    page = get_object_or_404(Page, slug="about")
    return render(request, "about.html", {"page": page})


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return render(request, "contact.html", {"form": ContactForm(), "success": True})
    return render(request, "contact.html", {"form": form})


def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            deposit_amount = appointment.service.price * Decimal("0.4")

            # same email sending block can go here too if you prefer

            return redirect("booking_success", appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, "book_appointment.html", {"form": form})


def booking_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    deposit_amount = appointment.service.price * Decimal("0.4")
    return render(
        request,
        "booking_success.html",
        {"appointment": appointment, "deposit_amount": deposit_amount},
    )

from django.db import models

class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Service(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,      # allow NULL in the database
        blank=True      # allow empty in forms/admin
    )

    def __str__(self):
        return self.name


class Testimonial(TimeStamped):
    client_name = models.CharField(max_length=120)
    service_type = models.CharField(max_length=120, blank=True)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)  # 1–5 stars
    show = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.client_name} ({self.rating}★)"

class GalleryImage(TimeStamped):
    title = models.CharField(max_length=150, blank=True)
    image = models.ImageField(upload_to='gallery/')
    is_hero = models.BooleanField(default=False)   # use on home hero slider
    is_services_banner = models.BooleanField(default=False)

    def __str__(self):
        return self.title or f"Image {self.pk}"

class Page(TimeStamped):
    """
    Simple CMS-like model for About, Introduction, History texts.
    Use slugs: about, introduction, history, contact_notice
    """
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=150)
    body = models.TextField()
    cover = models.ImageField(upload_to='pages/', blank=True, null=True)

    def __str__(self):
        return self.title





class SubService(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="subservices")
    name = models.CharField(max_length=100)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=False,  # ✅ subservices must have a price
        blank=False,
    )

    def __str__(self):
        return f"{self.service.name} - {self.name}"



 
class Appointment(TimeStamped):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    subservice = models.ForeignKey("SubService", on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)

    # ✅ new fields
    paid = models.BooleanField(default=False)
    paystack_ref = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name} – {self.service.name} on {self.date} {self.time}"
    
    @property
    def price(self):
        """Return correct price depending on service/subservice"""
        if self.service.price:  # For Manicure
            return self.service.price
        elif self.subservice:  # For Nails/Lashes/etc.
            return self.subservice.price
        return 0
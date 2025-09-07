import requests
from django.conf import settings

class Paystack:
    base_url = "https://api.paystack.co"

    def __init__(self):
        self.secret_key = settings.PAYSTACK_SECRET_KEY

    def initialize_payment(self, email, amount, reference, callback_url):
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        data = {
            "email": email,
            "amount": int(amount * 100),  # kobo
            "reference": reference,
            "callback_url": callback_url,
        }
        url = f"{self.base_url}/transaction/initialize"
        response = requests.post(url, json=data, headers=headers)
        return response.json()

    def verify_payment(self, reference):
        headers = {"Authorization": f"Bearer {self.secret_key}"}
        url = f"{self.base_url}/transaction/verify/{reference}"
        response = requests.get(url, headers=headers)
        return response.json()

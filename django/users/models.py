from django.db.models import EmailField, DecimalField
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = EmailField(unique=True)
    balance = DecimalField(max_digits=10, decimal_places=2, default=0.00)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
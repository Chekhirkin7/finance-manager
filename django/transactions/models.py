from django.db.models import DecimalField, ForeignKey, CharField, DateTimeField, Model, CASCADE
from django.conf import settings

class Transaction(Model):
    amount = DecimalField(decimal_places=2, max_digits=10)
    transaction_type = CharField(max_length=10, choices=[("income", "Income"), ("expense", "Expense")])
    category = CharField(max_length=100)
    created_at = DateTimeField(auto_now_add=True)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def __str__(self):
        return f"{self.amount} {self.transaction_type} - {self.category}"
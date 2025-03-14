from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.email")

    class Meta:
        model = Transaction
        fields = ("id", "user", "amount", "transaction_type", "category", "created_at")
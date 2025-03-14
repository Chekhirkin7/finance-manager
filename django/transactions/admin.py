from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "transaction_type", "category", "created_at")
    list_filter = ("transaction_type", "category")
    search_fields = ("user__email", "category")


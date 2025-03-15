from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Transaction
from .serializers import TransactionSerializer
from django.utils.dateparse import parse_date
from django.db.models import Sum
from rest_framework.decorators import action


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="summary")
    def summary(self, request):
        user = request.user

        total_income = Transaction.objects.filter(user=user, transaction_type="income").aggregate(Sum("amount"))["amount__sum"] or 0
        total_expense = Transaction.objects.filter(user=user, transaction_type="expense").aggregate(Sum("amount"))["amount__sum"] or 0
        balance = user.balance
        return Response({
            "total_income": total_income,
            "total_expense": total_expense,
            "balance": balance
        })

    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        params = self.request.query_params

        date = params.get("date")
        if date:
            parsed_date = parse_date(date)
            if parsed_date:
                queryset = queryset.filter(created_at__date=parsed_date)

        category = params.get("category")
        if category:
            queryset = queryset.filter(category=category)

        transaction_type = params.get("type")
        if transaction_type in ["income", "expense"]:
            queryset = queryset.filter(transaction_type=transaction_type)

        return queryset

    def perform_create(self, serializer):
        transaction = serializer.save(user=self.request.user)
        if transaction.transaction_type == "income":
            self.request.user.balance += transaction.amount
        else:
            self.request.user.balance -= transaction.amount
        self.request.user.save()

    def destroy(self, request, *args, **kwargs):
        transaction = self.get_object()

        if transaction.transaction_type == "income":
            request.user.balance -= transaction.amount
        else:
            request.user.balance += transaction.amount

        request.user.save()
        return super().destroy(request, *args, **kwargs)

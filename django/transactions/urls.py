from django.urls import path
from .views import TransactionViewSet

urlpatterns = [
    path("transactions/", TransactionViewSet.as_view({"get": "list", "post": "create"}), name="transactions-list"),
    path("transactions/<int:pk>/", TransactionViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}), name="transactions-detail"),
]

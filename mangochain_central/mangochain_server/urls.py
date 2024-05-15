# messages/urls.py
from django.urls import path
from .views import UserListCreateAPIView, store_block, TransactionListCreateAPIView

urlpatterns = [
    path('users', UserListCreateAPIView.as_view(), name='users-list-create'),
    path('blocks', store_block, name='blocks-list-create'),
    path('transactions', TransactionListCreateAPIView.as_view(), name='transactions-list-create'),
]

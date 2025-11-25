# search/urls.py

from django.urls import path
from .views import SearchListView

urlpatterns = [
    path('', SearchListView.as_view(), name='search'),
]
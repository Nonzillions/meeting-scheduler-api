from django.urls import path
from .views import FindSlotsView

urlpatterns = [
    path('find-slots/', FindSlotsView.as_view(), name='find-slots'),
]
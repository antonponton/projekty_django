from django.urls import path, reverse_lazy
from . import views

app_name='portfolio_marta'
urlpatterns = [
    path('', views.ArtListView.as_view(), name='all'),

]


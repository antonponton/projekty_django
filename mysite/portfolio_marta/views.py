from django.shortcuts import render
from portfolio_marta.models import Art
from django.views.generic import ListView

class ArtListView(ListView):
    model = Art
    template_name = "portfolio_marta/art_list.html"

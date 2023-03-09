from django.shortcuts import render
from portfolio_marta.models import Art

from django.views import View

class ArtListView(View):
    model = Art
    template_name = "portfolio_marta/art_list.html"

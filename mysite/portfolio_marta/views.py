from django.shortcuts import render
from portfolio_marta.models import Art
from portfolio_marta.forms import CreateForm
from portfolio_marta.owner import OwnerListView, OwnerDetailView, OwnerDeleteView

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime

class ArtListView(OwnerListView):
    model = Art
    template_name = "portfolio_marta/art_list.html"

class ArtDetailView(OwnerDetailView):
    model = Art
    template_name = "portfolio_marta/art_detail.html"

class ArtCreateView(LoginRequiredMixin, View):
    template_name = 'portfolio_marta/art_form.html'
    success_url = reverse_lazy('portfolio_marta:all')

    def get(self, request, pk=None):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        # Add owner to the model before saving
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        form.save_m2m()
        return redirect(self.success_url)
    

class ArtUpdateView(LoginRequiredMixin, View):
    template_name = 'portfolio_marta/art_form.html'
    success_url = reverse_lazy('portfolio_marta:all')

    def get(self, request, pk):
        pic = get_object_or_404(Art, id=pk, owner=self.request.user)
        form = CreateForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Art, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()
        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Art

def stream_file(request, pk):
    pic = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response
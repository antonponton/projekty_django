from django.shortcuts import render
from portfolio_marta.models import Art, Type, Comment
from portfolio_marta.forms import CreateForm, TypeForm, CommentForm
from portfolio_marta.owner import OwnerListView, OwnerDetailView, OwnerDeleteView

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin

class ArtListView(OwnerListView):
    model = Art
    template_name = "portfolio_marta/art_list.html"
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['type_list'] = Type.objects.all()
        return context

class ArtDetailView(OwnerDetailView):
    model = Art
    template_name = "portfolio_marta/art_detail.html"
    def get(self, request, pk) :
        x = Art.objects.get(id=pk)
        comments = Comment.objects.filter(art=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'art' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

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

class ArtDeleteView(OwnerDeleteView):
    model = Art

def stream_file(request, pk):
    pic = get_object_or_404(Art, id=pk)
    response = HttpResponse()
    response['Content-Type'] = pic.content_type
    response['Content-Length'] = len(pic.picture)
    response.write(pic.picture)
    return response

class TypeListView(OwnerListView):
    model = Type
    template_name = "portfolio_marta/type_list.html"

class TypeCreateView(LoginRequiredMixin, View):
    template_name = 'portfolio_marta/type_form.html'
    success_url = reverse_lazy('portfolio_marta:types')

    def get(self, request, pk=None):
        form = TypeForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        form = TypeForm(request.POST, request.FILES or None,)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        
        pic = form.save(commit=False)
        pic.owner = self.request.user
        pic.save()
        form.save_m2m()
        return redirect(self.success_url)

class TypeUpdateView(LoginRequiredMixin, View):
    template_name = 'portfolio_marta/type_form.html'
    success_url = reverse_lazy('portfolio_marta:types')

    def get(self, request, pk):
        pic = get_object_or_404(Type, id=pk, owner=self.request.user)
        form = TypeForm(instance=pic)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk=None):
        pic = get_object_or_404(Type, id=pk, owner=self.request.user)
        form = TypeForm(request.POST, request.FILES or None, instance=pic)

        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        pic = form.save(commit=False)
        pic.save()
        form.save_m2m()
        return redirect(self.success_url)

class TypeDeleteView(OwnerDeleteView):
    model = Type

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        a = get_object_or_404(Art, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, art=a)
        comment.save()
        return redirect(reverse('portfolio_marta:art_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "portfolio_marta/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        art = self.object.art
        return reverse('portfolio_marta:art_detail', args=[art.id])
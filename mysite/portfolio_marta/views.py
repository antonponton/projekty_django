from portfolio_marta.models import Art, Type, Comment, Fav
from portfolio_marta.forms import CreateForm, TypeForm, CommentForm, NewUserForm
from portfolio_marta.owner import OwnerListView, OwnerDetailView, OwnerDeleteView

from django.views import View
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.contrib.auth import login
from django.contrib import messages

class ArtListView(OwnerListView):
    model = Art
    template_name = "portfolio_marta/art_list.html"
    def get(self, request) :
        art_list = Art.objects.all()
        type_list = Type.objects.all()

        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
            rows = request.user.favorite_arts.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [ row['id'] for row in rows ]


        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            query.add(Q(tags__name__in=[strval]), Q.OR)
            art_list = Art.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else :
            art_list = Art.objects.all().order_by('-updated_at')[:10]

        # Augment the art_list
        for obj in art_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {'art_list' : art_list, 'favorites': favorites, 'search': strval, 'type_list' : type_list}
        return render(request, self.template_name, ctx)


class ArtDetailView(OwnerDetailView):
    model = Art
    template_name = "portfolio_marta/art_detail.html"
    def get(self, request, pk) :
        x = Art.objects.get(id=pk)
        comments = Comment.objects.filter(art=x).order_by('-updated_at')
        comment_form = CommentForm()
        context = { 'art' : x, 'comments': comments, 'comment_form': comment_form }
        return render(request, self.template_name, context)

class ArtCreateView(PermissionRequiredMixin, View):
    template_name = 'portfolio_marta/art_form.html'
    success_url = reverse_lazy('portfolio_marta:all')
    permission_required = ('portfolio_marta.add_art', 'portfolio_marta.change_art')

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
    

class ArtUpdateView(PermissionRequiredMixin, View):
    template_name = 'portfolio_marta/art_form.html'
    success_url = reverse_lazy('portfolio_marta:all')
    permission_required = ('portfolio_marta.add_art', 'portfolio_marta.change_art')

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

class TypeCreateView(PermissionRequiredMixin, View):
    template_name = 'portfolio_marta/type_form.html'
    success_url = reverse_lazy('portfolio_marta:types')
    permission_required = ('portfolio_marta.add_type', 'portfolio_marta.change_type')

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

class TypeUpdateView(PermissionRequiredMixin, View):
    template_name = 'portfolio_marta/type_form.html'
    success_url = reverse_lazy('portfolio_marta:types')
    permission_required = ('portfolio_marta.add_type', 'portfolio_marta.change_type')

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
    
# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Add PK",pk)
        a = get_object_or_404(Art, id=pk)
        fav = Fav(user=request.user, art=a)
        try:
            fav.save()  # In case of duplicate key
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        a = get_object_or_404(Art, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, art=a).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user, 'django.contrib.auth.backends.ModelBackend')
			messages.success(request, "Registration successful." )
			return redirect("portfolio_marta:all")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})
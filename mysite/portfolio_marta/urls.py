from django.urls import path, reverse_lazy
from . import views
from django.views.generic import TemplateView

app_name='portfolio_marta'
urlpatterns = [
    path('', views.ArtListView.as_view(), name='all'),
    path('info', TemplateView.as_view(template_name='portfolio_marta/info.html'), name="info"),
    path('contact', TemplateView.as_view(template_name='portfolio_marta/contact.html'), name="contact"),
    path('art/<int:pk>', views.ArtDetailView.as_view(), name='art_detail'),
    path('art/create',
        views.ArtCreateView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='art_create'),
    path('art/<int:pk>/update',
        views.ArtUpdateView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='art_update'),
    path('art/<int:pk>/delete',
        views.ArtDeleteView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='art_delete'),
    path('art_picture/<int:pk>', views.stream_file, name='art_picture'),
    path('types', views.TypeListView.as_view(), name='types'),
    path('type/create',
        views.TypeCreateView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='type_create'),
    path('type/<int:pk>/update',
        views.TypeUpdateView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='type_update'),
    path('type/<int:pk>/delete',
        views.TypeDeleteView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='type_delete'),
    path('art/<int:pk>/comment',
        views.CommentCreateView.as_view(), name='art_comment_create'),
    path('comment/<int:pk>/delete',
        views.CommentDeleteView.as_view(success_url=reverse_lazy('portfolio_marta')), name='art_comment_delete'),
    path('art/<int:pk>/favorite',
        views.AddFavoriteView.as_view(), name='art_favorite'),
    path('art/<int:pk>/unfavorite',
        views.DeleteFavoriteView.as_view(), name='art_unfavorite'),
]


from django.urls import path, reverse_lazy
from . import views

app_name='portfolio_marta'
urlpatterns = [
    path('', views.ArtListView.as_view(), name='all'),
    path('art/<int:pk>', views.ArtDetailView.as_view(), name='art_detail'),
    path('art/create',
        views.ArtCreateView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='art_create'),
    path('art/<int:pk>/update',
        views.ArtUpdateView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='art_update'),
    path('art/<int:pk>/delete',
        views.ArtDeleteView.as_view(success_url=reverse_lazy('portfolio_marta:all')), name='art_delete'),
    path('art_picture/<int:pk>', views.stream_file, name='art_picture'),
]


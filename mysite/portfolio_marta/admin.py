from django.contrib import admin
from portfolio_marta.models import Art, Type, Fav, Comment
# Register your models here.

admin.site.register(Art)
admin.site.register(Type)
admin.site.register(Fav)
admin.site.register(Comment)
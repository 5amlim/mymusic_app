from django.contrib import admin

# Register your models here.
from .models import Music, Session, Artist, Photo

admin.site.register(Music)
admin.site.register(Session)
admin.site.register(Artist)
admin.site.register(Photo)
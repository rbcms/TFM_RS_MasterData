"""
Creo el admin para mi TFM

"""
from django.contrib import admin
from .models import Post

admin.site.register(Post)
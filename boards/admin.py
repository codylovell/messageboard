from django.contrib import admin

# Register your models here.

# Allow boards to be created in /admin
from .models import Board

admin.site.register(Board)
""""Customized Admin"""
from django.contrib import admin
from.models import Place

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """"Class for displaying custom place model on admin site"""
    fields = ['user', 'name', 'description']
    list_display = ('user', 'name')
    search_fields = ['name']
    
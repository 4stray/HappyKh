""""Customized Admin"""
from django.contrib import admin
from .models import Place, Address


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    """"Class for displaying custom place model on admin site"""
    fields = ['user', 'name', 'address', 'description']
    list_display = ('name', 'address')
    search_fields = ['name']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """"Class for displaying custom adress model on admin site"""
    fields = ['address', 'latitude', 'longitude']
    list_display = ('address',)
    search_fields = ['address']
    ordering = ('address',)

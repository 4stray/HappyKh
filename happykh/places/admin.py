""""Customized Admin"""
from django.contrib import admin
from .models import Place, Address, CommentPlace


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


@admin.register(CommentPlace)
class CommentPlaceAdmin(admin.ModelAdmin):
    """"Class for displaying custom CommentPlace model on admin site"""
    fields = ['creator', 'creation_time', 'text', 'place']
    list_display = ('creator', 'creation_time', 'text', 'place')
    ordering = ('-creation_time',)

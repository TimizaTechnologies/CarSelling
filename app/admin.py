from django.contrib import admin
from .models import Car
from .models import Contact
from .models import Team
from django.utils.html import format_html

# Register your models here.
class CarAdmin(admin.ModelAdmin):
    readonly_fields = ('thumbnail_preview',)

    def thumbnail_preview(self, obj):
        return obj.thumbnail_preview

    thumbnail_preview.short_description= 'Thumbnail Preview'
    thumbnail_preview.allow_tags = True

    list_display = ('id', 'thumbnail_preview', 'car_title', 'color', 'year', 'body_style', 'fuel_type', 'is_featured')
    list_display_links= ('id', 'thumbnail_preview', 'car_title')
    list_editable=('is_featured',)
    search_fields= ('id', 'car_title', 'color', 'fuel_type')
    list_filter= ('car_title', 'color', 'year', 'body_style', 'fuel_type')

admin.site.register(Car, CarAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display=('id', 'first_name', 'last_name', 'email', 'car_title', 'city', 'create_date')
    list_display_links=('id', 'first_name', 'last_name')
    search_fields=('first_name', 'last_name', 'email', 'car_title')
    list_per_page=25


admin.site.register(Contact, ContactAdmin)

class TeamAdmin(admin.ModelAdmin):
    # def thumbnail(self, object):
    #     return format_html('<img src="{}" width="40"/>'.format(object.photo.url))
    #
    # thumbnail.short_description='Photo'
    # fields=('first_name', 'designation')
    list_display=['id', 'first_name', 'designation']
    list_display_links=['id', 'first_name']
    search_fields=['first_name', 'designation', 'last_name']
    list_filter=['designation']

admin.site.register(Team, TeamAdmin)
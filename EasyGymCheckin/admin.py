from django.contrib import admin
from .models import gymClass, gymClient, gymCheckin

admin.site.register(gymClass)
admin.site.register(gymClient)
admin.site.register(gymCheckin)

from django.contrib import admin
from .models import nodes, temperature, humidity

# Register your models here.
admin.site.register(nodes)
admin.site.register(temperature)
admin.site.register(humidity)
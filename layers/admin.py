from django.contrib import admin
from layers.models import Layer

class LayerAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Layer)

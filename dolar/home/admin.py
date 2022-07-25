from django.contrib import admin
from .models import Cotizacion

# Register your models here.
# admin.site.register(Cotizacion)

class CotizacionAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Currency', {'fields': ['currency', 'name']}),
        ('Date information', {'fields': ['datetime']}),
        ('Values', {'fields': ['buy', 'sell', 'other']}),
    ]
    list_display = ('datetime', 'currency', 'name')

admin.site.register(Cotizacion, CotizacionAdmin)
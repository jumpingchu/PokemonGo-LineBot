from django.contrib import admin
from pokemongogo.models import CounterInfo

# Register your models here.
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'cName', 'cCategory', 'cUrl')
    list_filter = ('cCategory',)
    search_fields = ('cName', 'cCategory',)
    ordering = ('id',)

admin.site.register(CounterInfo, PokemonAdmin)
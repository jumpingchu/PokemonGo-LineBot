from django.contrib import admin
from pokemongogo.models import CounterInfo
from pokemongogo.models import News
from pokemongogo.models import PttArticles


# Register your models here.
class PokemonAdmin(admin.ModelAdmin):
    list_display = ('id', 'cName', 'cCategory', 'cUrl')
    list_filter = ('cCategory',)
    search_fields = ('cName', 'cCategory',)
    ordering = ('id',)

admin.site.register(CounterInfo, PokemonAdmin)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'cName', 'cDate', 'cUrl')
    list_filter = ('cDate',)
    search_fields = ('cName',)
    ordering = ('-id',)

admin.site.register(News, NewsAdmin)
admin.site.register(PttArticles, NewsAdmin)

from django.contrib import admin
from .models import Events


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'dateInitial', 'dateFinal', 'location', 'description', 'user')
    search_fields = ('title', 'dateInitial', 'dateFinal', 'location', 'description', 'user')


admin.site.register(Events, EventAdmin)
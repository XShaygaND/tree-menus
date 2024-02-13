from django.contrib import admin
from django.contrib.admin.widgets import ForeignKeyRawIdWidget

from .models import MenuItem


class MenuItemInline(admin.StackedInline):
    model = MenuItem
    fk_name = 'parent'
    widgets = {
        'parent': ForeignKeyRawIdWidget(MenuItem, 'name'),
    }

    def get_exclude(self, request, obj=None):
        return ['name', 'depth', 'url'] # Will be defaulted in the models `save`


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [MenuItemInline]
    list_display = ('name', 'title', 'parent', 'depth')
    list_filter = ('name',)
    readonly_fields = ('depth', 'name')
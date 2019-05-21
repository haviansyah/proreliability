from django.contrib import admin

from .models import *

admin.site.register(Unit)
admin.site.register(Condition)
admin.site.register(Standard)

@admin.register(Equipment)
class Equipment(admin.ModelAdmin):
    def get_unit(self, obj):
        return obj.Unit.name
    def get_condition(self, obj):
        return obj.Condition.name

    search_fields = ['name']
    list_display = ('id','name','get_condition','get_unit')
    list_filter = ('Unit__name','Condition__name')


@admin.register(Header)
class Header(admin.ModelAdmin):
    def get_equipment(self, obj):
        return obj.Equipment.name
    def get_unit(self, obj):
        return obj.Equipment.Unit.name
    def get_condition(self, obj):
        return obj.Equipment.Condition.name

    search_fields = ['name']
    list_editable = ('hitung',)
    list_display = ('name','get_equipment','get_condition','get_unit','hitung')
    list_filter = ('Equipment__name','Equipment__Unit__name','Equipment__Condition__name')

@admin.register(MonitoringRow)
class AuthorAdmin(admin.ModelAdmin):
    def get_equipment(self, obj):
        return obj.Equipment.name
    def get_unit(self, obj):
        return obj.Equipment.Unit.name
    def get_condition(self, obj):
        return obj.Equipment.Condition.name
    date_hierarchy = 'tanggal'
    search_fields = ['Equipment']
    list_display = ('tanggal','get_equipment','get_condition','get_unit')
    list_filter = ('Equipment__name','Equipment__Unit__name','Equipment__Condition__name')


admin.site.register(MonitoringData)

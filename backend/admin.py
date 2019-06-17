from django.contrib import admin
from django import forms
from django.forms import ModelChoiceField

from .models import *

admin.site.register(Unit)
admin.site.register(Condition)
admin.site.register(AlatDCS)
admin.site.register(AssetWellness)
admin.site.register(Standard)


class ModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class AlatUnitChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.AlatDCS.name,obj.Unit.name)


class TagDcsForm(forms.ModelForm):
    AlatUnitDCS = AlatUnitChoiceField(queryset=AlatUnitDCS.objects.all())
    class Meta :
        model = DcsTag
        fields = '__all__'


class AlatUnitDcsForm(forms.ModelForm):
    Unit = ModelChoiceField(queryset=Unit.objects.all())
    AlatDCS = ModelChoiceField(queryset=AlatDCS.objects.all())
    class Meta :
        model = AlatUnitDCS
        fields = '__all__'


@admin.register(DcsTag)
class DcsTag(admin.ModelAdmin):
    def Unit(self,obj):
        return obj.AlatUnitDCS.Unit.name
    def Alat(self,obj):
        return obj.AlatUnitDCS.AlatDCS.name
    form = TagDcsForm
    list_display = ('Unit','Alat','tag','left','top','satuan')
    list_filter = ('AlatUnitDCS__AlatDCS__name','AlatUnitDCS__Unit__name')


@admin.register(AlatUnitDCS)
class AlatUnitDCS(admin.ModelAdmin):
    def get_unit(self, obj):
        return obj.Unit.name
    def Alat(self, obj):
        return obj.AlatDCS.name

    list_display = ('Alat', 'get_unit')
    form = AlatUnitDcsForm


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

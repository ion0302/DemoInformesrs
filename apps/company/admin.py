from django.contrib import admin
from django import forms
from apps.company.models import Plan, Rule, PlanLog, RequestLog


class RuleResourceSelect(forms.Select):
    pass


class RuleForm(forms.ModelForm):
    class Meta:
        model = Rule
        fields = '__all__'
        widgets = {'resource': RuleResourceSelect}


class RuleInline(admin.TabularInline):
    model = Rule
    form = RuleForm


class PlanAdmin(admin.ModelAdmin):
    inlines = [
        RuleInline,
    ]


admin.site.register(Plan, PlanAdmin)

admin.site.register(Rule)
admin.site.register(PlanLog)
admin.site.register(RequestLog)

from django.contrib import admin
from django import forms
from apps.company.models import Plan, Rule, PlanLog, RequestLog

from apps.company.views import CompanyViewSet, PlanLogViewSet
from rest_framework.routers import SimpleRouter


def get_actions():
    router = SimpleRouter()
    routes = router.get_routes(CompanyViewSet)
    resource_list = []
    for route in routes:
        resource = [f'Company.{res}' for res in list(route.mapping.values())]
        resource_list += resource

    return [(resource, resource.upper()) for resource in resource_list]


class RuleForm(forms.ModelForm):
    resource = forms.ChoiceField(choices=get_actions())


class RuleInline(admin.TabularInline):
    model = Rule
    form = RuleForm


class PlanAdmin(admin.ModelAdmin):
    inlines = [
        RuleInline,
    ]


class RuleAdmin(admin.ModelAdmin):
    form = RuleForm


admin.site.register(Plan, PlanAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(PlanLog)
admin.site.register(RequestLog)

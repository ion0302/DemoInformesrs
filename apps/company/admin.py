from django.contrib import admin
from apps.company.models import Plan, Rule, PlanLog

admin.site.register(Plan)
admin.site.register(Rule)
admin.site.register(PlanLog)


from django.contrib import admin
from apps.company.models import Plan, Rule, PlanLog, RequestLog

admin.site.register(Plan)
admin.site.register(Rule)
admin.site.register(PlanLog)
admin.site.register(RequestLog)


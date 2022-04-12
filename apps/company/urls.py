from rest_framework.routers import DefaultRouter

from apps.company.views import PlanViewSet, RuleViewSet, CompanyViewSet, PlanLogViewSet

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plans')
router.register('rules', RuleViewSet, basename='rules')
router.register('planlogs', PlanLogViewSet, basename='planlogs')
router.register('companies', CompanyViewSet, basename='companies')

urlpatterns = router.urls
